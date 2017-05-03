# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

from tool.io import get_query_stats_file, write_to_txt, get_env_stats_file
from tool.experiment import QUERY, Q_PLAY, Q_MOVE, OPERATOR_LIST, RAN,\
    CONSEQ, ENDSEQ, MINSEQ, MAXSEQ, MAX, MIN
from tool.query.stream import get_register_stream, REG_Q_STR


# =============================================================================
# Queries with preference operators
# =============================================================================
# Play
Q_SEQ = '''
SEQUENCE IDENTIFIED BY pid [RANGE {ran} SECOND] FROM s\n
'''

Q_CONSEQ = '''
SUBSEQUENCE CONSECUTIVE TIMESTAMP FROM\n
'''

Q_ENDSEQ = '''
SUBSEQUENCE END POSITION FROM\n
'''

Q_MINSEQ = '''
MINIMUM LENGTH IS {min}
'''

Q_MAXSEQ = '''
MAXIMUM LENGTH IS {max}
'''

Q_PLAY_BESTSEQ = '''
\nACCORDING TO TEMPORAL PREFERENCES
IF PREVIOUS (pl = 're') THEN
    (pl = 'dr') BETTER (pl = 'cp') [pc]
AND
    (pl = 'cp') BETTER (pl = 'ncp')
AND
IF ALL PREVIOUS (pc = 'mf') THEN
    (pc = 'mf') BETTER (pc = 'di')
;
'''

# Move
Q_MOVE_BESTSEQ = '''
ACCORDING TO TEMPORAL PREFERENCES
IF PREVIOUS (pc = 'di') AND (tb = 1) THEN
    (pc = 'mf') BETTER (pc = 'di')[mv]
AND
IF ALL PREVIOUS (tb = 1) AND (tb = 0) AND PREVIOUS (pc = 'oi') THEN
    (pc = 'mf') BETTER (pc = 'oi')
AND
(mv = 'la') BETTER (mv = 'fw')
;
'''


def gen_stats_query(configuration, experiment_conf):
    '''
    Generate streampref queries
    '''
    op_list = experiment_conf[OPERATOR_LIST]
    query = 'SELECT '
    # ENDSEQ
    if ENDSEQ in op_list:
        query += Q_ENDSEQ
    # CONSEQ
    if CONSEQ in op_list:
        query += Q_CONSEQ
    # SEQ
    query += Q_SEQ.format(ran=experiment_conf[RAN])
    where_list = []
    # MINSEQ
    if MINSEQ in op_list:
        where_list.append(Q_MINSEQ.format(min=experiment_conf[MIN]))
    # MAXSEQ
    if MAXSEQ in op_list:
        where_list.append(Q_MAXSEQ.format(max=experiment_conf[MAX]))
    if len(where_list):
        query += '\nWHERE ' + ' AND '.join(where_list)
    # Select correct query
    if experiment_conf[QUERY] == Q_PLAY:
        query += Q_PLAY_BESTSEQ
    elif experiment_conf[QUERY] == Q_MOVE:
        query += Q_MOVE_BESTSEQ
    # Store query code
    filename = get_query_stats_file(configuration, experiment_conf)
    write_to_txt(filename, query)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    # For every experiment
    for exp_conf in experiment_list:
        # Generate appropriate queries
        gen_stats_query(configuration, exp_conf)


def gen_stats_env(configuration, experiment_conf):
    '''
    Generate environment files for SEQ operator
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    filename = get_query_stats_file(configuration, experiment_conf)
    # Register query
    text += REG_Q_STR.format(qname='stats', qfile=filename)
    # Get environment filename
    filename = get_env_stats_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_all_env(configuration, experiment_list):
    '''
    Generate all environment files
    '''
    for exp_conf in experiment_list:
        gen_stats_env(configuration, exp_conf)
