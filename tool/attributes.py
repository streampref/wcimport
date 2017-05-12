# -*- coding: utf-8 -*-
'''
Attributes
'''

# =============================================================================
# System attributes
# =============================================================================
TS_ATT = '_ts'
FL_ATT = '_fl'

# =============================================================================
# Original attributes
# =============================================================================
MINUTE = 'min'
SECOND = 'sec'
PLAYER_ID = 'player_id'
X = 'x'
Y = 'y'
TYPE = 'type'
TO_X = 'to_x'
TO_Y = 'to_y'
TO_Z = 'to_z'
PERIOD = 'period'
TEAM = 'team'
OUTCOME = 'outcome'
FIELD_PASS = 'field_pass'
SIDE = 'side'

# =============================================================================
# Translated attributes
# =============================================================================
PID = 'pid'  # Player ID
PLACE = 'pc'
TEAM_BALL = 'tb'
MOVE = 'mv'
PLAY = 'pl'

# =============================================================================
# Domains of translated attributes
# =============================================================================

DOM_DICT = {}
DOM_DICT[PLACE] = ['da', 'di', 'mf', 'oi', 'oa']
DOM_DICT[PLAY] = ['ca', 'cp', 'dr', 'lb', 'ncp', 're', 'o']
DOM_DICT[MOVE] = ['fw', 'rw', 'la']
DOM_DICT[TEAM_BALL] = [0, 1]

# =============================================================================
# Player and team attributes
# =============================================================================
ID = 'id'
NAME = 'name'
ISO = 'iso'
REAL_POSITION = 'real_position'
REAL_POSITION_SIDE = 'real_position_side'
KNOWN_NAME = 'known_name'
SHORT_NAME = 'short_name'
LAST_NAME = 'last_name'
FIRST_NAME = 'first_name'
MIDDLE_NAME = 'middle_name'
TEAM_ID = 'team_id'
PREFERRED_FOOT = 'preferred_foot'
CLUB = 'club'
CAPS = 'caps'
GOALS = 'goals'
JERSEY_NUM = 'jersey_num'
COUNTRY = 'country'
BIRTH_DATE = 'birth_date'
PPOSITION = 'position'

# =============================================================================
#  Attribute Types
# =============================================================================
STRING = 'STRING'
INT = 'INTEGER'
FLOAT = 'FLOAT'

# =============================================================================
#  Attribute Lists
# =============================================================================
# Original attribute list
ORIGINAL_ATT_LIST = [MINUTE, SECOND, PLAYER_ID, X, Y, TYPE, TO_X, TO_Y,
                     TO_Z, PERIOD, TEAM, OUTCOME, FIELD_PASS, SIDE]
# Move attribute list
MOVE_ATT_LIST = [PID, PLACE, TEAM_BALL, MOVE]
# Play attribute list
PLAY_ATT_LIST = [PID, PLACE, PLAY]
# Player attribute list
PLAYER_ATT_LIST = [ID, NAME, REAL_POSITION, REAL_POSITION_SIDE,
                   KNOWN_NAME, SHORT_NAME, LAST_NAME, FIRST_NAME,
                   MIDDLE_NAME, TEAM_ID, PREFERRED_FOOT, CLUB, CAPS, GOALS,
                   JERSEY_NUM, COUNTRY, BIRTH_DATE, PPOSITION]
# Team attribute list
TEAM_ATT_LIST = [ID, NAME, ISO]

# =============================================================================
#  Attribute Types (excluding timestamp)
# =============================================================================
# Plays: PID, PLACE, PLAY
PLAY_TYPE_LIST = [INT, STRING, STRING]
# Moves: PID, PLACE, TEAM_BALL, MOVE
MOVE_TYPE_LIST = [INT, STRING, INT, STRING]


def _process_attribute_list(attribute_list, prefix='', timestamp=False,
                            flag=False):
    '''
    Process an attribute list to include prefix, timestamp and flag
    '''
    att_list = attribute_list[:]
    if prefix != '':
        att_list = [prefix + att for att in att_list]
    if flag:
        att_list.insert(0, FL_ATT)
    if timestamp:
        att_list.insert(0, TS_ATT)
    return att_list


def get_original_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of original attributes
    '''
    return _process_attribute_list(ORIGINAL_ATT_LIST, prefix, timestamp, flag)


def get_play_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of play attributes
    '''
    return _process_attribute_list(PLAY_ATT_LIST, prefix, timestamp, flag)


def get_move_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of move attributes
    '''
    return _process_attribute_list(MOVE_ATT_LIST, prefix, timestamp, flag)


def get_player_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of player attributes
    '''
    return _process_attribute_list(PLAYER_ATT_LIST, prefix, timestamp, flag)


def get_team_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of player attributes
    '''
    return _process_attribute_list(TEAM_ATT_LIST, prefix, timestamp, flag)


def get_play_attributes_and_types():
    '''
    Return the list of play attributes and types
    '''
    att_list = zip(PLAY_ATT_LIST, PLAY_TYPE_LIST)
    att_list = [att + ' ' + att_type for (att, att_type) in att_list]
    return att_list


def get_move_attributes_and_types():
    '''
    Return the list of move attributes and types
    '''
    att_list = zip(MOVE_ATT_LIST, MOVE_TYPE_LIST)
    att_list = [att + ' ' + att_type for (att, att_type) in att_list]
    return att_list
