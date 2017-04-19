#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module to import data of soccer world cup of 2014 from
http://data.huffingtonpost.com
'''

from tool.attributes import TS_ATT, MINUTE, SECOND, PLAYER_ID, X, Y, TYPE, \
    OUTCOME, PID, PLACE, TEAM_BALL, MOVE, PLAY, FL_ATT, \
    get_original_attribute_list,\
    get_player_attribute_list
from tool.io import create_import_directory, get_match_json, \
    decode_object, get_match_players_json, get_match_list, store_full_data,\
    store_move_data, store_play_data, store_players


def get_all_matches(match_id_list):
    '''
    Get all data from http://data.huffingtonpost.com
    '''
    print 'Getting matches data'
    match_dict = {}
    for match_id in match_id_list:
        print 'Getting data for match ' + match_id
        match_data = get_match_json(match_id)
        match_data = decode_object(match_data)
        if match_data is not None:
            match_dict[match_id] = match_data
    return match_dict


def get_all_players(match_id_list):
    '''
    Get all data from http://data.huffingtonpost.com
    '''
    print 'Getting players data'
    attributes_set = set()
    player_dict = {}
    # For every match
    for match_id in match_id_list:
        print 'Getting player for match ' + match_id
        # Get match players
        match_player_list = get_match_players_json(match_id)
        # Decode player objects
        match_player_list = decode_object(match_player_list)
        # For every player
        for player in match_player_list:
            # Update set of all attributes
            attributes_set = attributes_set.union(set(player.keys()))
            player_id = player['id']
            player[PLAYER_ID] = player_id
            # Check if player was not processed
            if player_id not in player_dict:
                # Add player do dictionary
                player_dict[player_id] = player
    print 'Removing duplicated players'
    # List of non duplicated players
    player_list = []
    # For every player
    for player in player_dict.values():
        new_player = {}
        for att in get_player_attribute_list():
            if att in player:
                new_player[att] = player[att]
            else:
                new_player[att] = ''
        new_player[TS_ATT] = 0
        new_player[FL_ATT] = '+'
        player_list.append(new_player)
    return player_list


def remove_duplicates(record_list):
    '''
    Return a new record list without duplicated PID per instant
    '''
    # Create new record list
    rec_list = []
    # Create set of processed
    processed_set = set()
    # For every input record
    for rec in record_list:
        # Convert record to tuple
        tup = (TS_ATT, rec[TS_ATT], PID, rec[PID])
        # Check if tuple was already processed
        if tup not in processed_set:
            # Add to processed
            processed_set.add(tup)
            # Add to result list
            rec_list.append(rec)
    return rec_list


def calculate_move_stream(event_list):
    '''
    Calculate move stream
    '''
    player_event_dict = {}
    # Separate event of each player
    for event in event_list:
        player_id = event[PLAYER_ID]
        # Check if player ID does no exists
        if player_id not in player_event_dict:
            # Create a list for this player
            player_event_dict[player_id] = []
        p_event = {TS_ATT: event[TS_ATT], PID: player_id,
                   X: event[X], Y: event[Y]}
        # Position
        if event[X] < 20:
            p_event[PLACE] = 'da'
        elif event[X] < 35:
            p_event[PLACE] = 'di'
        elif event[X] < 65:
            p_event[PLACE] = 'mf'
        elif event[X] < 80:
            p_event[PLACE] = 'oi'
        else:
            p_event[PLACE] = 'oa'
        # Ball possession
        p_event[TEAM_BALL] = event[OUTCOME]
        player_event_dict[player_id].append(p_event)
    new_event_list = []
    # For every player
    for player_id in player_event_dict:
        # Sort player events by timestamp
        p_event_list = sorted(player_event_dict[player_id],
                              key=lambda k: k[TS_ATT])
        prev_event = p_event_list.pop(0)
        while len(p_event_list):
            cur_event = p_event_list.pop(0)
            # Final event
            new_event = {TS_ATT: cur_event[TS_ATT], PID: player_id,
                         PLACE: cur_event[PLACE],
                         TEAM_BALL: cur_event[TEAM_BALL]}
            # Calculate move
            x_dist = cur_event[X] - prev_event[X]
            y_dist = cur_event[Y] - prev_event[Y]
            if abs(y_dist) > abs(x_dist):
                new_event[MOVE] = 'la'
            elif x_dist > 0:
                new_event[MOVE] = 'fw'
            else:
                new_event[MOVE] = 'rw'
            new_event_list.append(new_event)
    # Remove duplicated
    new_event_list = remove_duplicates(new_event_list)
    # Sort all events by timestamp
    return sorted(new_event_list, key=lambda k: k[TS_ATT])


def calculate_play_stream(event_list):  # IGNORE:too-many-branches
    '''
    Calculate play stream
    '''
    new_event_list = []
    for event in event_list:
        new_event = {TS_ATT: event[TS_ATT], PID: event[PLAYER_ID]}
        # Position
        if event[X] < 20:
            new_event[PLACE] = 'da'
        elif event[X] < 35:
            new_event[PLACE] = 'di'
        elif event[X] < 65:
            new_event[PLACE] = 'mf'
        elif event[X] < 80:
            new_event[PLACE] = 'oi'
        else:
            new_event[PLACE] = 'oa'
        # Play
        # Other (for unknown type)
        new_event[PLAY] = 'o'
        # Carry (conduction)
        if event[TYPE] == '101':
            new_event[PLAY] = 'ca'
        # Completed pass
        elif event[TYPE] == '1' and event[OUTCOME] == '1':
            new_event[PLAY] = 'cp'
        # Not completed pass
        elif event[TYPE] == '1' and event[OUTCOME] == '0':
            new_event[PLAY] = 'ncp'
        # Dribble
        elif event[TYPE] in ['3', '42'] and event[OUTCOME] == '1':
            new_event[PLAY] = 'dr'
        # Lost ball
        elif event[TYPE] in ['45', '50', '51', '57']:
            new_event[PLAY] = 'lb'
        elif event[TYPE] in ['3', '42', '61'] and event[OUTCOME] == '0':
            new_event[PLAY] = 'lb'
        # Reception
        elif event[TYPE] == '100':
            new_event[PLAY] = 're'
        new_event_list.append(new_event)
    # Remove duplicated
    new_event_list = remove_duplicates(new_event_list)
    # Sort all events by timestamp
    return sorted(new_event_list, key=lambda k: k[TS_ATT])


def get_match_events(match_data):
    '''
    Select necessary attributes from original event data
    '''
    event_list = match_data['events']
    new_event_list = []
    for event in event_list:
        new_event = {}
        for att in get_original_attribute_list():
            new_event[att] = event[att]
        timestamp = new_event[MINUTE] * 60 + new_event[SECOND]
        new_event[TS_ATT] = timestamp
        new_event_list.append(new_event)
    return sorted(new_event_list, key=lambda k: k[TS_ATT])


def store_match_events_csv(match_dict):
    '''
    Store matches data into CSV files
    '''
    print 'Storing events data'
    for match_id in match_dict:
        print 'Store events for match ' + match_id
        match_data = match_dict[match_id]
        # Store original data
        rec_list = get_match_events(match_data)
        store_full_data(match_id, rec_list)
        # Move stream
        new_rec_list = calculate_move_stream(rec_list)
        store_move_data(match_id, new_rec_list)
        # Play stream
        new_rec_list = calculate_play_stream(rec_list)
        store_play_data(match_id, new_rec_list)


def main():
    '''
    Main routine
    '''
    # Create directories
    create_import_directory()
    # Get list of matches
    match_id_list = get_match_list()
    # Get matches data
    match_dict = get_all_matches(match_id_list)
    # Store match events into csv files
    store_match_events_csv(match_dict)
    # Get players data
    player_list = get_all_players(match_id_list)
    print 'Storing players data into csv files'
    store_players(player_list)


if __name__ == '__main__':
    main()
