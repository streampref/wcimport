#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module to import data of 2014 Soccer World Cup from
http://data.huffingtonpost.com
'''

from tool.attributes import TS_ATT, MINUTE, SECOND, PLAYER_ID, X, Y, TYPE, \
    OUTCOME, PLACE, BALL_POSS, DIRECTION, MOVE, FL_ATT, \
    get_event_attribute_list,\
    get_player_attribute_list, ID, NAME, ISO, DA, DI, MF, OI, OA, FIELD_PASS,\
    NONE, LATERAL, FORWARD, BACKWARD, TYPEOUT_TO_MOVE
from tool.io import create_import_directory, get_match_json, \
    decode_object, get_match_players_json, get_match_list, store_event_data,\
    store_place_data, store_move_data, store_players, get_match_teams_json,\
    store_teams


def get_all_matches(match_list):
    '''
    Get all matches
    '''
    print 'Getting matches data'
    match_dict = {}
    for match in match_list:
        match_id = match[ID]
        print 'Getting data for match ' + match_id
        match_data = get_match_json(match_id)
        match_data = decode_object(match_data)
        if match_data is not None:
            match_dict[match_id] = match_data
    return match_dict


def get_all_players(match_dict):
    '''
    Get all players
    '''
    print 'Getting players data'
    attributes_set = set()
    player_dict = {}
    # For every match
    for match_id in match_dict:
        print 'Getting player for match ' + match_id
        # Get match players
        match_player_list = get_match_players_json(match_id)
        # Decode player objects
        match_player_list = decode_object(match_player_list)
        # For every player
        for player in match_player_list:
            # Update set of all attributes
            attributes_set = attributes_set.union(set(player.keys()))
            player_id = player[ID]
            # Check if player was not processed
            if player_id not in player_dict:
                # Add player do dictionary
                player_dict[player_id] = player
            else:
                player_dict[player_id].update(player)
    print 'Processing player attributes'
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


def get_all_teams(match_dict):
    '''
    Get all teams
    '''
    print 'Getting teams data'
    attributes_set = set()
    teams_dict = {}
    # For every match
    for match_id in match_dict:
        print 'Getting teams for match ' + match_id
        # Get match players
        match_team_list = get_match_teams_json(match_id)
        # Decode player objects
        match_team_list = decode_object(match_team_list)
        # For every player
        for team in match_team_list:
            # Update set of all attributes
            attributes_set = attributes_set.union(set(team.keys()))
            team_id = team[ID]
            # Check if player was not processed
            if team_id not in teams_dict:
                # Add player do dictionary
                teams_dict[team_id] = {ID: team[ID],
                                       NAME: team[NAME],
                                       ISO: team[ISO],
                                       TS_ATT: 0,
                                       FL_ATT: '+'}
    return teams_dict.values()


def remove_duplicates(record_list):
    '''
    Return a new record list without duplicated player per instant
    '''
    # Create new record list
    rec_list = []
    # Create set of processed
    processed_set = set()
    # For every input record
    for rec in record_list:
        # Convert record to tuple
        tup = (TS_ATT, rec[TS_ATT], PLAYER_ID, rec[PLAYER_ID])
        # Check if tuple was already processed
        if tup not in processed_set:
            # Add to processed
            processed_set.add(tup)
            # Add to result list
            rec_list.append(rec)
    return rec_list


def calc_place(x_coord):
    '''
    Calculate place according to x coordinate
    '''
    if x_coord < 20:
        return DA
    elif x_coord < 35:
        return DI
    elif x_coord < 65:
        return MF
    elif x_coord < 80:
        return OI
    else:
        return OA


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
        p_event = {TS_ATT: event[TS_ATT], PLAYER_ID: player_id,
                   X: event[X], Y: event[Y]}
        # Place
        p_event[PLACE] = calc_place(event[X])
        # Ball possession
        if event[FIELD_PASS] == 't':
            p_event[BALL_POSS] = 1
        else:
            p_event[BALL_POSS] = 0
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
            new_event = {TS_ATT: cur_event[TS_ATT], PLAYER_ID: player_id,
                         PLACE: cur_event[PLACE],
                         BALL_POSS: cur_event[BALL_POSS]}
            # Calculate move
            x_dist = cur_event[X] - prev_event[X]
            y_dist = cur_event[Y] - prev_event[Y]
            if x_dist == 0 and y_dist == 0:
                new_event[DIRECTION] = NONE
            elif abs(y_dist) > abs(x_dist):
                new_event[DIRECTION] = LATERAL
            elif x_dist > 0:
                new_event[DIRECTION] = FORWARD
            else:
                new_event[DIRECTION] = BACKWARD
            new_event_list.append(new_event)
    # Remove duplicated
    new_event_list = remove_duplicates(new_event_list)
    # Sort all events by timestamp
    return sorted(new_event_list, key=lambda k: k[TS_ATT])


def calc_move(move_type, outcome):
    '''
    Calculate move according to type and outcome attributes
    '''
    if (move_type, outcome) in TYPEOUT_TO_MOVE:
        return TYPEOUT_TO_MOVE[(move_type, outcome)]
    else:
        return None


def calculate_play_stream(event_list):  # IGNORE:too-many-branches
    '''
    Calculate play stream
    '''
    new_event_list = []
    for event in event_list:
        new_event = {TS_ATT: event[TS_ATT], PLAYER_ID: event[PLAYER_ID]}
        # Place
        new_event[PLACE] = calc_place(event[X])
        # Play
        new_event[MOVE] = calc_move(int(event[TYPE]), int(event[OUTCOME]))
        if new_event[MOVE] is not None:
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
        for att in get_event_attribute_list():
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
        store_event_data(match_id, rec_list)
        # Move stream
        new_rec_list = calculate_move_stream(rec_list)
        store_place_data(match_id, new_rec_list)
        # Play stream
        new_rec_list = calculate_play_stream(rec_list)
        store_move_data(match_id, new_rec_list)


def main():
    '''
    Main routine
    '''
    # Create directories
    create_import_directory()
    # Get list of matches
    match_list = get_match_list()
    # Get matches data
    match_dict = get_all_matches(match_list)
    # Store match events into csv files
    store_match_events_csv(match_dict)
    # Get teams data
    team_list = get_all_teams(match_dict)
    print 'Storing teams data into csv files'
    store_teams(team_list)
    # Get players data
    player_list = get_all_players(match_dict)
    print 'Storing players data into csv files'
    store_players(player_list)


if __name__ == '__main__':
    main()
