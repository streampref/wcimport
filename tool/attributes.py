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
# Player attributes
# =============================================================================
NAME = 'name'
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
PLAYER_ATT_LIST = [PID, NAME, REAL_POSITION, REAL_POSITION_SIDE,
                   KNOWN_NAME, SHORT_NAME, LAST_NAME, FIRST_NAME,
                   MIDDLE_NAME, TEAM_ID, PREFERRED_FOOT, CLUB, CAPS, GOALS,
                   JERSEY_NUM, COUNTRY, BIRTH_DATE, PPOSITION]

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

# def get_attribute_list(query_id, prefix='', include_timestamp=False):
#     '''
#     Return a list of attributes
#     '''
#     # Select attribute list
#     if query_id == Q1:
#         att_list = PLAY_ATT_LIST[:]
#     elif query_id == Q2:
#         att_list = MOVE_ATT_LIST[:]
#     if prefix != '':
#         att_list = [prefix + att for att in att_list]
#     # Include timestamp attribute at beginning
#     if include_timestamp:
#         att_list.insert(0, TS)
#     return att_list
#
#
# def get_attributes_and_types(query_id):
#     '''
#     Return attributes and types from lists of attributes and types
#     '''
#     # Select attribute list
#     if query_id == Q1:
#         att_list = PLAY_ATT_LIST[:]
#         type_list = PLAY_TYPE_LIST[:]
#     elif query_id == Q2:
#         att_list = MOVE_ATT_LIST[:]
#     att_str_list = []
#     for index, att in enumerate(att_list):
#         att_str_list.append(att + ' ' + type_list[index])
#     return att_str_list
