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
# Attributes
# =============================================================================
ATTENDANCE = 'attendance'    # Match
BIRTH_DATE = 'birth_date'    # Player
CAPS = 'caps'                # Player
CLUB = 'club'                # Player
COUNTRY = 'country'          # Player
DATE = 'date'                # Match
FIELD_PASS = 'field_pass'    # Event
FIRST_NAME = 'first_name'    # Player
GOALS = 'goals'              # Player
ID = 'id'                    # Match, Team and Player
ISO = 'iso'                  # Team
JERSEY_NUM = 'jersey_num'    # Player
KNOWN_NAME = 'known_name'    # Player
LAST_NAME = 'last_name'      # Player
MIDDLE_NAME = 'middle_name'  # Player
MINUTE = 'min'               # Event
DIRECTION = 'direc'          # Place
NAME = 'name'                # Player
OUTCOME = 'outcome'          # Event
PERIOD = 'period'            # Event
PLACE = 'place'              # Move and Place
MOVE = 'move'                # Move
PLAYER_ID = 'player_id'      # Event, Move and Place
PPOSITION = 'position'       # Player
PREFERRED_FOOT = 'preferred_foot'  # Player
REAL_POSITION = 'real_position'  # Player
REAL_POSITION_SIDE = 'real_position_side'  # Player
SECOND = 'sec'               # Event
SHORT_NAME = 'short_name'    # Player
SIDE = 'side'                # Event
TEAM = 'team'                # Event
BALL_POSS = 'ball'           # Place
TEAM_ID = 'team_id'          # Player
TIME = 'time'                # Match
TO_X = 'to_x'                # Event
TO_Y = 'to_y'                # Event
TO_Z = 'to_z'                # Event
TYPE = 'type'                # Event
VENUE = 'venue'              # Match
X = 'x'                      # Event
Y = 'y'                      # Event

# =============================================================================
# Places
# =============================================================================
DA = 'da'
DI = 'di'
MF = 'mf'
OI = 'oi'
OA = 'oa'

# =============================================================================
# Moves
# =============================================================================
BAD_PASS = 'bpas'
BALL_OUT = 'bout'
BALL_RECOVERY = 'brec'
CLEARANCE = 'clea'
CONDUCTION = 'cond'
DRIBBLE = 'drib'
DRIBBLED = 'dled'
FOUL = 'foul'
FOUL_SUFFERED = 'fsuf'
GOAL = 'goal'
GOALKEEPER_SAVE = 'gsav'
INTERCEPTION = 'int'
LOST_BALL = 'lbal'
PASS = 'pass'
RECEPTION = 'rec'
WRONG_SHOT = 'wsho'

# =============================================================================
# Move mapping
# =============================================================================
TYPEOUT_TO_MOVE = {
    (1, 1): PASS, (59, 1): PASS,
    (1, 0): BAD_PASS, (2, 1): BAD_PASS,
    (3, 0): LOST_BALL, (7, 0): LOST_BALL, (44, 0): LOST_BALL,
    (50, 1): LOST_BALL, (51, 1): LOST_BALL, (57, 0): LOST_BALL,
    (59, 0): LOST_BALL, (61, 0): LOST_BALL,
    (3, 1): DRIBBLE, (42, 1): DRIBBLE,
    (4, 0): FOUL,
    (4, 1): FOUL_SUFFERED, (55, 1): FOUL_SUFFERED,
    (45, 0): DRIBBLED,
    (5, 0): BALL_OUT, (6, 0): BALL_OUT,
    (7, 1): BALL_RECOVERY, (44, 1): BALL_RECOVERY, (49, 1): BALL_RECOVERY,
    (56, 1): BALL_RECOVERY, (61, 1): BALL_RECOVERY,
    (8, 1): INTERCEPTION, (74, 1): INTERCEPTION,
    (10, 1): GOALKEEPER_SAVE, (11, 1): GOALKEEPER_SAVE,
    (41, 1): GOALKEEPER_SAVE, (52, 1): GOALKEEPER_SAVE,
    (54, 1): GOALKEEPER_SAVE,
    (12, 1): CLEARANCE,
    (13, 1): WRONG_SHOT, (14, 1): WRONG_SHOT, (15, 1): WRONG_SHOT,
    (16, 1): GOAL,
    (100, 1): RECEPTION,
    (101, 1): CONDUCTION
}
# =============================================================================
# Directions
# =============================================================================
BACKWARD = 'bw'
FORWARD = 'fw'
LATERAL = 'la'
NONE = 'no'

# =============================================================================
# Domains of translated attributes
# =============================================================================
DOM_DICT = {}
DOM_DICT[PLACE] = [DA, DI, MF, OI, OA]
DOM_DICT[MOVE] = [BAD_PASS, BALL_OUT, BALL_RECOVERY, CLEARANCE, CONDUCTION,
                  DRIBBLE, DRIBBLED, FOUL, FOUL_SUFFERED, GOAL,
                  GOALKEEPER_SAVE, INTERCEPTION, LOST_BALL, PASS, RECEPTION,
                  WRONG_SHOT]
DOM_DICT[DIRECTION] = [BACKWARD, FORWARD, LATERAL, NONE]
DOM_DICT[BALL_POSS] = [0, 1]

# =============================================================================
#  Attribute Types
# =============================================================================
STRING = 'STRING'
INT = 'INTEGER'
FLOAT = 'FLOAT'

# =============================================================================
#  Attribute Lists
# =============================================================================
# Event attribute list
EVENT_ATT_LIST = [MINUTE, SECOND, PLAYER_ID, X, Y, TYPE, TO_X, TO_Y,
                  TO_Z, PERIOD, TEAM, OUTCOME, FIELD_PASS, SIDE]
# Place attribute list
PLACE_ATT_LIST = [PLAYER_ID, PLACE, BALL_POSS, DIRECTION]
# Move attribute list
MOVE_ATT_LIST = [PLAYER_ID, PLACE, MOVE]
# Player attribute list
PLAYER_ATT_LIST = [ID, NAME, REAL_POSITION, REAL_POSITION_SIDE,
                   KNOWN_NAME, SHORT_NAME, LAST_NAME, FIRST_NAME,
                   MIDDLE_NAME, TEAM_ID, PREFERRED_FOOT, CLUB, CAPS, GOALS,
                   JERSEY_NUM, COUNTRY, BIRTH_DATE, PPOSITION]
# Team attribute list
TEAM_ATT_LIST = [ID, NAME, ISO]
# Match attribute list
MATCH_ATT_LIST = [ID, DATE, TIME, VENUE, ATTENDANCE]

# =============================================================================
#  Attribute Types (excluding timestamp)
# =============================================================================
# Move: PLAYER_ID, PLACE, MOVE
MOVE_TYPE_LIST = [INT, STRING, STRING]
# Place: PLAYER_ID, PLACE, BALL_POSS, DIRECTION
PLACE_TYPE_LIST = [INT, STRING, INT, STRING]


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


def get_event_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of event attributes
    '''
    return _process_attribute_list(EVENT_ATT_LIST, prefix, timestamp, flag)


def get_move_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of move attributes
    '''
    return _process_attribute_list(MOVE_ATT_LIST, prefix, timestamp, flag)


def get_place_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of place attributes
    '''
    return _process_attribute_list(PLACE_ATT_LIST, prefix, timestamp, flag)


def get_player_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of player attributes
    '''
    return _process_attribute_list(PLAYER_ATT_LIST, prefix, timestamp, flag)


def get_team_attribute_list(prefix='', timestamp=False, flag=False):
    '''
    Return list of team attributes
    '''
    return _process_attribute_list(TEAM_ATT_LIST, prefix, timestamp, flag)


def get_move_attributes_and_types():
    '''
    Return the list of move attributes and types
    '''
    att_list = zip(MOVE_ATT_LIST, MOVE_TYPE_LIST)
    att_list = [att + ' ' + att_type for (att, att_type) in att_list]
    return att_list


def get_place_attributes_and_types():
    '''
    Return the list of place attributes and types
    '''
    att_list = zip(PLACE_ATT_LIST, PLACE_TYPE_LIST)
    att_list = [att + ' ' + att_type for (att, att_type) in att_list]
    return att_list
