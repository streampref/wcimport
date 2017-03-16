# -*- coding: utf-8 -*-
'''
Directories, files, URL
'''
import csv
import json
import os
from bs4 import BeautifulSoup
from kitchen.text.converters import to_str

from tool.attributes import ORIGINAL_ATT_LIST, MOVE_ATT_LIST, \
    PLACEMENT_ATT_LIST, PLAY_ATT_LIST, PLAYER_ATT


# =============================================================================
# URL
# =============================================================================
# Start URL (final match)
START_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/' + \
    'germany-vs-argentina-731830'
# URL for JSON data of match
JSON_DATA_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/%s.json'
# URL for HTML data of match
HTML_DATA_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/%s'

# =============================================================================
# DIRECTORIES
# =============================================================================
# Imported data directory
IMPORTED_DATA_DIR = 'wc_data'
# Main directory for JSON files
JSON_DIR = IMPORTED_DATA_DIR + os.sep + 'json'
# Directory for original data
MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'match_full'
# Directory for move data
MOVE_MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'move'
# Directory for placement data
PLACEMENT_MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'placement'
# Directory for play data
PLAY_MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'play'
# Directories list
DIR_LIST = [IMPORTED_DATA_DIR, JSON_DIR, MATCH_DIR,
            MOVE_MATCH_DIR, PLACEMENT_MATCH_DIR, PLAY_MATCH_DIR]


# =============================================================================
# Files
# =============================================================================
# File with list of matches
MATCH_LIST_FILE = IMPORTED_DATA_DIR + os.sep + 'matches.txt'
# File with the list of players
PLAYER_FILE = IMPORTED_DATA_DIR + os.sep + 'players.csv'

# =============================================================================
# Others
# =============================================================================
# Number of retries to get an URL
URL_RETRY = 10

# Register dialect for CSV files
csv.register_dialect('table', delimiter='|', skipinitialspace=True)


def read_url(url):
    '''
    Try to get an URL content
    '''
    import requests
    from time import sleep
    print 'Reading URL: ' + url
    try_count = 0
    while try_count < URL_RETRY:
        content = None
        try:
            # Try to read URL
            content = requests.get(url)
        except Exception as exc:  # IGNORE:broad-except
            # Print exceptions
            print '\n Error for ' + url
            print exc
            print 'Retry\n'
            sleep(1)
        # Try to read the URL content
        if content is not None:
            # Check if content status is OK
            if content.status_code == 200:
                return content.text
            else:
                # Print errors
                print '\nError for ' + url
                print 'Error code: ' + str(content.status_code)
                print 'Retry\n'
                sleep(1)
        try_count += 1
    # Return empty string when the URL could not be read
    return None


def write_csv_file(record_list, filename, attribute_list):
    '''
    Write record list into file
    '''
    # Check if record list is not empty
    if not len(record_list):
        return
    # Open file
    out_file = open(filename, 'w')
    # Check if attribute list is None
    if attribute_list is None:
        # Extract attribute list from record list
        attribute_list = record_list[0].keys()
    # Write data
    out_write = csv.DictWriter(out_file, attribute_list, dialect='table')
    out_write.writeheader()
    out_write.writerows(record_list)
    out_file.close()


def create_directories():
    '''
    Create default directories if they do not exists
    '''
    print 'Creating directories'
    for directory in DIR_LIST:
        if not os.path.exists(directory):
            os.mkdir(directory)


def store_match_list(match_id_list):
    '''
    Store match list into a file
    '''
    match_file = open(MATCH_LIST_FILE, 'w')
    for match in match_id_list:
        match_file.write(match + '\n')
    match_file.close()


def get_match_id_list_from_file():
    '''
    Get list of matches identifier from file
    '''
    if os.path.isfile(MATCH_LIST_FILE):
        print 'Reading list of matches from ' + MATCH_LIST_FILE
        match_file = open(MATCH_LIST_FILE, 'r')
        match_id_list = []
        for line in match_file:
            match_id_list.append(line.strip())
        match_file.close()
        return match_id_list
    else:
        return None


def get_match_id_list():
    '''
    Return a list of identifiers to matches
    '''
    print 'Getting list of matches'
    # Try to read the match list from file
    link_list = get_match_id_list_from_file()
    if link_list is not None:
        # Return the list read from file
        return link_list
    link_list = []
    # Read site content
    content = read_url(START_URL)
    # Parse site content
    soup = BeautifulSoup(content, 'html.parser')
    # Find correct tag
    tag_list = soup.find_all("span", class_="matchup")
    # Search for links to others matches
    for tag in tag_list:
        # Check if tag is a tag
        a_list = tag.find_all('a')
        # Get link
        for item in a_list:
            link = item.get('href')
            # Get just final part of link
            link = link.split('/')[-1]
            if link not in link_list:
                link_list.append(link)
    # Sort matches by numerical ID
    match_id_list = sorted(link_list, key=lambda k: int(k.split('-')[-1]))
    # Store match list
    store_match_list(match_id_list)
    return match_id_list


def decode_object(original_object):
    '''
    Decode a dictionary to string
    '''
    # Check if object is unicode
    if isinstance(original_object, unicode):
        return to_str(original_object)
    # Check if object is dictionary
    elif isinstance(original_object, dict):
        new_dict = {}
        # Decode every dictionary entry
        for key in original_object:
            new_key = decode_object(key)
            value = original_object[key]
            new_value = decode_object(value)
            new_dict[new_key] = new_value
        return new_dict
    # Check if object is a list
    elif isinstance(original_object, list):
        new_list = []
        # Decode every list entry
        for item in original_object:
            new_item = decode_object(item)
            new_list.append(new_item)
        return new_list
    elif original_object is None:
        return 'NaN'
    return original_object


def get_match_json(match):
    '''
    Get JSON data from a match
    '''
    filename = JSON_DIR + os.sep + match + '.json'
    # Check if match was already imported
    if os.path.isfile(filename):
        print 'Reading already imported data from ' + filename
        # Just read data file of match
        json_file = open(filename, 'r')
        match_data = json.loads(json_file.read())
        json_file.close()
        return match_data
    # Download data
    match_id = match.split('-')[-1]
    url = JSON_DATA_URL % match_id
    content = read_url(url)
    if content is not None:
        # Store content on file
        print 'Storing imported data to ' + filename
        json_file = open(filename, 'wb')
        match_data = json.loads(content)
        json.dump(match_data, json_file, indent=2)
        json_file.close()
        return match_data
    return None


def get_match_players_json(match_id):
    '''
    Get JSON data of players
    '''
    filename = JSON_DIR + os.sep + match_id + '-players.json'
    if os.path.isfile(filename):
        print 'Reading already imported data from ' + filename
        # Just read data file of match
        json_file = open(filename, 'r')
        player_data = json.loads(json_file.read())
        json_file.close()
        return player_data
    url = HTML_DATA_URL % match_id
    content = read_url(url)
    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        # Get second script block
        data_script = soup.findAll("script")[1]
        data_lines = data_script.text.split('\n')
        # Scan all lines
        for line in data_lines:
            # Check if line has the player data
            if len(line) > 14 and line[:14] == 'HPIN.players =':
                # Get list of players
                line_data = line.split(' = ')[1]
                # Remove ';' at end
                line_data = line_data[:-1]
                player_data = json.loads(line_data)
                print 'Storing imported data to ' + filename
                json_file = open(filename, 'wb')
                json.dump(player_data, json_file, indent=2)
                json_file.close()
                return player_data
    return None


def store_full_data(match_id, record_list):
    '''
    Store full match data
    '''
    filename = MATCH_DIR + os.sep + match_id + '.csv'
    write_csv_file(record_list, filename, ORIGINAL_ATT_LIST)


def store_move_data(match_id, record_list):
    '''
    Store match moves
    '''
    filename = MOVE_MATCH_DIR + os.sep + match_id + '.csv'
    write_csv_file(record_list, filename, MOVE_ATT_LIST)


def store_placement_data(match_id, record_list):
    '''
    Store match placements
    '''
    filename = PLACEMENT_MATCH_DIR + os.sep + match_id + '.csv'
    write_csv_file(record_list, filename, PLACEMENT_ATT_LIST)


def store_play_data(match_id, record_list):
    '''
    Store match plays
    '''
    filename = PLAY_MATCH_DIR + os.sep + match_id + '.csv'
    write_csv_file(record_list, filename, PLAY_ATT_LIST)


def store_players(record_list):
    '''
    Store player data
    '''
    write_csv_file(record_list, PLAYER_FILE, PLAYER_ATT)
