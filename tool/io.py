# -*- coding: utf-8 -*-
'''
Directories, files, URL
'''
import csv
import json
import os
from bs4 import BeautifulSoup
from kitchen.text.converters import to_str

from tool.attributes import TS_ATT, get_event_attribute_list, \
    get_place_attribute_list, get_move_attribute_list, \
    get_player_attribute_list, get_team_attribute_list, ID, MATCH_ATT_LIST
from tool.experiment import QUERY_LIST, DIRECTORY, ALGORITHM, \
    QUERY, ALGORITHM_LIST, get_id, get_stats_id


# =============================================================================
# URL
# =============================================================================
BASE_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/'
# Start URL (final match)
START_URL = BASE_URL + \
    'germany-vs-argentina-731830'
# URL for JSON data of match
JSON_DATA_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/%s.json'
# URL for HTML data of match
HTML_DATA_URL = 'http://data.huffingtonpost.com/2014/world-cup/matches/%s'

# =============================================================================
# Directories for imported data
# =============================================================================
# Imported data directory
IMPORTED_DATA_DIR = 'data'
# Main directory for JSON files
JSON_DIR = IMPORTED_DATA_DIR + os.sep + 'raw'
# Directory for original data
MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'events'
# Directory for move data
PLACE_MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'places'
# Directory for play data
MOVE_MATCH_DIR = IMPORTED_DATA_DIR + os.sep + 'moves'
# Directories list
IMPORT_DIR_LIST = [IMPORTED_DATA_DIR, JSON_DIR, MATCH_DIR,
                   PLACE_MATCH_DIR, MOVE_MATCH_DIR]

# =============================================================================
# Generic directories and files for experiments
# =============================================================================
QUERY_DIR = 'queries'
ENV_DIR = 'env'
OUT_DIR = 'out'
OUT_AUX_DIR = 'out_aux'
DETAIL_DIR = 'details'
SUMMARY_DIR = 'summary'
RESULT_DIR = 'result'
EXPERIMENT_DIR_LIST = [QUERY_DIR, ENV_DIR, OUT_DIR, OUT_AUX_DIR,
                       DETAIL_DIR, SUMMARY_DIR, RESULT_DIR]

# =============================================================================
# Main directories
# =============================================================================
# SEQ operator
SEQ_MAIN_DIR = 'exp_seq'
# BESTSEQ operator
BESTSEQ_MAIN_DIR = 'exp_bestseq'
# CONSEQ operator
CONSEQ_MAIN_DIR = 'exp_conseq'
# ENDSEQ operator
ENDSEQ_MAIN_DIR = 'exp_endseq'
# MINSEQ operator
MINSEQ_MAIN_DIR = 'exp_minseq'
# MAXSEQ operator
MAXSEQ_MAIN_DIR = 'exp_maxseq'
# Statistics experiments
STATS_MAIN_DIR = 'exp_stats'

# =============================================================================
# Files
# =============================================================================
# File with list of matches
MATCH_LIST_FILE = IMPORTED_DATA_DIR + os.sep + 'matches.csv'
# File with the list of players
PLAYER_FILE = IMPORTED_DATA_DIR + os.sep + 'players.csv'
# File with the list of teams
TEAM_FILE = IMPORTED_DATA_DIR + os.sep + 'teams.csv'

# =============================================================================
# Others
# =============================================================================
# Number of retries to get an URL
URL_RETRY = 10


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


def _create_directories(directory_list):
    '''
    Create a list of directories if they do not exists
    '''
    print 'Creating directories'
    for directory in directory_list:
        if not os.path.exists(directory):
            os.mkdir(directory)


def create_import_directory():
    '''
    Create directories for data importing
    '''
    _create_directories(IMPORT_DIR_LIST)


def create_experiment_directories(configuration, experiment_list):
    '''
    Create directories for experiments
    '''
    # Get main directory
    main_dir = configuration[DIRECTORY]
    # Get list of queries
    query_list = configuration[QUERY_LIST]
    # Add main directory to directory list
    dir_list = [main_dir]
    # For every query
    for query in query_list:
        # Add "main_dir"/"query" to list
        dir_list.append(main_dir + os.sep + query)
        # For every sub_dir in experiment list
        for subdir in EXPERIMENT_DIR_LIST:
            # Add "main_dir"/"query"/"sub_dir" to list
            direc = main_dir + os.sep + query + os.sep + subdir
            dir_list.append(direc)
        # Create environment, query, detail and output directories
        for alg in configuration[ALGORITHM_LIST]:
            # Add "main_dir"/"query"/"env_dir"/"algorithm" to list
            direc = main_dir + os.sep + query + os.sep + ENV_DIR + os.sep + alg
            dir_list.append(direc)
            # Add "main_dir"/"query"/"out_dir"/"algorithm" to list
            direc = main_dir + os.sep + query + os.sep + OUT_DIR + os.sep + alg
            dir_list.append(direc)
            # Add "main_dir"/"query"/"detail_dir"/"algorithm" to list
            direc = \
                main_dir + os.sep + query + os.sep + DETAIL_DIR + os.sep + alg
            dir_list.append(direc)
            # Add "main_dir"/"query"/"query_dir"/"algorithm" to list
            direc = \
                main_dir + os.sep + query + os.sep + QUERY_DIR + os.sep + alg
            dir_list.append(direc)
            # Add sub_dir for queries
            for exp in experiment_list:
                exp_id = get_id(configuration, exp)
                # Add "main_dir"/"query"/"query_dir"/"algorithm"/"exp_id"
                direc = main_dir + os.sep + query + os.sep + QUERY_DIR + \
                    os.sep + alg + os.sep + exp_id
                dir_list.append(direc)
            # Add sub_dir for auxiliary output
            direc = \
                main_dir + os.sep + query + os.sep + OUT_AUX_DIR + os.sep + alg
            dir_list.append(direc)
            for exp in experiment_list:
                exp_id = get_id(configuration, exp)
                # Add "main_dir"/"query"/"query_dir"/"algorithm"/"exp_id"
                direc = main_dir + os.sep + query + os.sep + OUT_AUX_DIR + \
                    os.sep + alg + os.sep + exp_id
                dir_list.append(direc)
    _create_directories(dir_list)


def create_stat_exp_directories(configuration):
    '''
    Create directories for statistical experiments
    '''
    # Get main directory
    main_dir = configuration[DIRECTORY]
    # Get list of queries
    query_list = configuration[QUERY_LIST]
    # Add main directory to directory list
    dir_list = [main_dir]
    # For every query
    for query in query_list:
        # Add "main_dir"/"query" to list
        dir_list.append(main_dir + os.sep + query)
        # For every sub_dir in experiment list
        for subdir in EXPERIMENT_DIR_LIST:
            # Add "main_dir"/"query"/"sub_dir" to list
            direc = main_dir + os.sep + query + os.sep + subdir
            dir_list.append(direc)
    _create_directories(dir_list)


def store_match_list(match_list):
    '''
    Store match list into a file
    '''
    write_to_csv(MATCH_LIST_FILE, MATCH_ATT_LIST, match_list)


def get_match_list_from_file():
    '''
    Get list of matches from file
    '''
    if os.path.isfile(MATCH_LIST_FILE):
        print 'Reading list of matches from ' + MATCH_LIST_FILE
        match_list = read_from_csv(MATCH_LIST_FILE, MATCH_ATT_LIST)
        return match_list
    else:
        return None


def get_match_id_list():
    '''
    Return a list of match identifiers
    '''
    match_list = get_match_list()
    return [match[ID] for match in match_list]


def get_match_list():
    '''
    Return the list of matches
    '''
    print 'Getting list of matches'
    # Try to read the match list from file
    link_list = get_match_list_from_file()
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
            link = to_str(link.split('/')[-1])
            if link not in link_list:
                link_list.append(link)
    # Sort matches by numerical ID
    match_id_list = sorted(link_list, key=lambda k: int(k.split('-')[-1]))
    match_list = []
    for match_id in match_id_list:
        match_dict = get_match_details(match_id)
        new_match_dict = {}
        for att in MATCH_ATT_LIST:
            if att in match_dict:
                new_match_dict[att] = match_dict[att]
            else:
                new_match_dict[att] = ''
        match_list.append(new_match_dict)
    # Store match list
    store_match_list(match_list)
    return match_list


def get_match_details(match_id):
    '''
    Get match details
    '''
    url = BASE_URL + match_id
    # Read site content
    content = read_url(url)
    # Parse site content
    soup = BeautifulSoup(content, 'html.parser')
    detail = soup.find_all("div", class_="module match-meta")
    det_list = detail[0].ul.find_all('li')
    det_dict = {ID: to_str(match_id)}
    for det_item in det_list:
        det_str = det_item.get_text()
        det = det_str.split(':')
        det_id = to_str(det[0]).lower().strip()
        det_value = to_str(det[1]).lower().strip()
        det_dict[det_id] = det_value
    return det_dict


def decode_object(original_object):
    '''
    Decode unicode to string
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


def get_match_teams_json(match_id):
    '''
    Get JSON data of teams
    '''
    filename = JSON_DIR + os.sep + match_id + '-teams.json'
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
            if len(line) > 12 and line[:12] == 'HPIN.teams =':
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


def get_event_data_file(match_id):
    '''
    Get file name of event
    '''
    return MATCH_DIR + os.sep + match_id + '.csv'


def store_event_data(match_id, record_list):
    '''
    Store event data
    '''
    filename = get_event_data_file(match_id)
    att_list = get_event_attribute_list(timestamp=True)
    write_to_csv(filename, att_list, record_list)


def get_move_data_file(match_id):
    '''
    Get file name of move
    '''
    return MOVE_MATCH_DIR + os.sep + match_id + '.csv'


def store_move_data(match_id, record_list):
    '''
    Store match moves
    '''
    filename = get_move_data_file(match_id)
    att_list = get_move_attribute_list(timestamp=True)
    write_to_csv(filename, att_list, record_list)


def get_place_data_file(match_id):
    '''
    Get file name of place
    '''
    return PLACE_MATCH_DIR + os.sep + match_id + '.csv'


def store_place_data(match_id, record_list):
    '''
    Store place data
    '''
    filename = get_place_data_file(match_id)
    att_list = get_place_attribute_list(timestamp=True)
    write_to_csv(filename, att_list, record_list)


def store_players(record_list):
    '''
    Store players data
    '''
    att_list = get_player_attribute_list(timestamp=True, flag=True)
    write_to_csv(PLAYER_FILE, att_list, record_list)


def store_teams(record_list):
    '''
    Store teams data
    '''
    att_list = get_team_attribute_list(timestamp=True, flag=True)
    write_to_csv(TEAM_FILE, att_list, record_list)


def write_to_txt(filename, text):
    '''
    Store record list into a TXT file
    '''
    # Check if file does not exists
    if not os.path.isfile(filename):
        # Store data to file
        out_file = open(filename, 'w')
        out_file.write(text)
        out_file.close()


def get_query_dir(configuration, experiment_conf):
    '''
    Return query directory
    '''
    exp_id = get_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + QUERY_DIR + os.sep + experiment_conf[ALGORITHM] + \
        os.sep + exp_id


def get_query_stats_file(configuration, experiment_conf):
    '''
    Return query filename for statistics query
    '''
    exp_id = get_stats_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + QUERY_DIR + os.sep + exp_id + '.cql'


def get_env_stats_file(configuration, experiment_conf):
    '''
    Return environment filename for statistics query
    '''
    exp_id = get_stats_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + ENV_DIR + os.sep + exp_id + '.env'


def get_out_file(configuration, experiment_conf):
    '''
    Return output file
    '''
    exp_id = get_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + OUT_DIR + os.sep + experiment_conf[ALGORITHM] + \
        os.sep + exp_id + '.csv'


def get_aux_out_file(configuration, experiment_conf, query_id):
    '''
    Return auxiliary output file
    '''
    exp_id = get_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + OUT_AUX_DIR + os.sep + experiment_conf[ALGORITHM] + \
        os.sep + exp_id + os.sep + query_id + '.csv'


def get_env_file(configuration, experiment_conf):
    '''
    Return environment file
    '''
    exp_id = get_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + ENV_DIR + os.sep + experiment_conf[ALGORITHM] + \
        os.sep + exp_id + '.env'


def get_summary_file(configuration, query, summary, parameter):
    '''
    Return summary file
    '''
    if summary != '':
        summary += '_'
    return configuration[DIRECTORY] + os.sep + query + os.sep + \
        SUMMARY_DIR + os.sep + summary + parameter + '.csv'


def get_result_file(configuration, query, summary, parameter):
    '''
    Return result file
    '''
    return configuration[DIRECTORY] + os.sep + query + os.sep + \
        RESULT_DIR + os.sep + summary + '_' + parameter + '.csv'


def get_detail_file(configuration, experiment_conf, count):
    '''
    Return detail file
    '''
    exp_id = get_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + DETAIL_DIR + os.sep + experiment_conf[ALGORITHM] + \
        os.sep + exp_id + ':' + str(count) + '.csv'


def get_detail_stats_file(configuration, experiment_conf):
    '''
    Return statistics detail file
    '''
    exp_id = get_stats_id(configuration, experiment_conf)
    return configuration[DIRECTORY] + os.sep + experiment_conf[QUERY] + \
        os.sep + DETAIL_DIR + os.sep + exp_id + '.csv'


def get_tup_file(query):
    '''
    Get the TUP filename
    '''
    return IMPORTED_DATA_DIR + os.sep + 'tup_' + query + '.csv'


def write_result_file(filename, record_list, key_field):
    '''
    Write to a result file
    '''
    # Check if there exists records to be stored
    if len(record_list):
        # Get the field list
        field_list = [field for field in record_list[0].keys()
                      if field != key_field]
        # Sort the field list
        field_list.sort()
        # Put key field in the beginning of field list
        field_list.insert(0, key_field)
        write_to_csv(filename, field_list, record_list)


def write_to_csv(filename, attribute_list, record_list):
    '''
    Store record list into a CSV file
    '''
    # Check if file does not exists
    if not os.path.isfile(filename):
        # Store data to file
        data_file = open(filename, 'w')
        csv.register_dialect('pipes', delimiter='|', skipinitialspace=True)
        writer = csv.DictWriter(data_file, attribute_list, dialect='pipes')
        writer.writeheader()
        writer.writerows(record_list)
        data_file.close()


def read_from_csv(filename, attribute_list):
    '''
    Read data from a CSV file
    '''
    data_file = open(filename, 'r')
    csv.register_dialect('pipes', delimiter='|', skipinitialspace=True)
    reader = csv.DictReader(data_file, attribute_list, dialect='pipes')
    # Skip header
    reader.next()
    rec_list = []
    for rec in reader:
        rec_list.append(rec)
    return rec_list


def get_max_move_ts(match_id):
    '''
    Return the maximum timestamp from move stream
    '''
    filename = get_move_data_file(match_id)
    att_list = get_move_attribute_list(timestamp=True)
    rec_list = read_from_csv(filename, att_list)
    last_rec = rec_list[-1]
    return int(last_rec[TS_ATT])


def get_max_place_ts(match_id):
    '''
    Return the maximum timestamp from place stream
    '''
    filename = get_place_data_file(match_id)
    att_list = get_place_attribute_list(timestamp=True)
    rec_list = read_from_csv(filename, att_list)
    last_rec = rec_list[-1]
    return int(last_rec[TS_ATT])
