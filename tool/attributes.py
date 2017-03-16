# -*- coding: utf-8 -*-
'''
Attributes
'''

# =============================================================================
# System attributes
# =============================================================================
TS = '_ts'
FL = '_fl'

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
ORIGINAL_ATT_LIST = [TS, MINUTE, SECOND, PLAYER_ID, X, Y, TYPE, TO_X, TO_Y,
                     TO_Z, PERIOD, TEAM, OUTCOME, FIELD_PASS, SIDE]
# Move attribute list
MOVE_ATT_LIST = [TS, PID, PLACE, TEAM_BALL, MOVE]
# Placement attribute list
PLACEMENT_ATT_LIST = [TS, PID, PLACE, TEAM_BALL]
# Play attribute list
PLAY_ATT_LIST = [TS, PID, PLACE, PLAY]
# Player attribute list
PLAYER_ATT = [TS, FL, PID, NAME, REAL_POSITION, REAL_POSITION_SIDE,
              KNOWN_NAME, SHORT_NAME, LAST_NAME, FIRST_NAME,
              MIDDLE_NAME, TEAM_ID, PREFERRED_FOOT, CLUB, CAPS, GOALS,
              JERSEY_NUM, COUNTRY, BIRTH_DATE, PPOSITION]

# =============================================================================
#  Attribute Types (excluding timestamp)
# =============================================================================
# Placement: PID, PLACE, TEAM_BALL
PLACEMENT_TYPE_LIST = [INT, STRING, INT]
# Plays: PID, PLACE, PLAY
PLAY_TYPE_LIST = [INT, STRING, STRING]
# Moves: PID, PLACE, TEAM_BALL, MOVE
MOVE_TYPE_LIST = [INT, STRING, INT, STRING]
