# -*- coding: utf-8 -*-
'''
Queries for experiments with SEQ operator
'''

import os

from tool.attributes import get_move_attribute_list, get_place_attribute_list
from tool.experiment import SLI, RAN, ALGORITHM, \
    CQL_ALG, QUERY, Q_MOVE, Q_PLACE
from tool.io import get_query_dir, write_to_txt, get_out_file, get_env_file
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR


# =============================================================================
# Query using SEQ operator
# =============================================================================
SEQ_QUERY = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s;
'''

# =============================================================================
# CQL Equivalent Queries
# =============================================================================
# RPOS (_pos attribute with original timestamp)
CQL_RPOS = 'SELECT _ts AS _pos, * FROM s[RANGE 1 SECOND, SLIDE 1 SECOND];'
# SPOS (convert RPOS back to stream format)
CQL_SPOS = 'SELECT RSTREAM FROM rpos;'
# W (Window of tuples from SPOS)
CQL_W = '''
SELECT _pos, {att}
FROM spos[RANGE {ran} SECOND, SLIDE {sli} SECOND];
'''
# W_1 (Sequence positions from 1 to end)
CQL_W1 = 'SELECT _pos, player_id FROM w;'
# W_i (Sequence positions from i to end,  w_(i-1) - p_(i-1))
CQL_WI = '''
SELECT * FROM w{prev}
EXCEPT
SELECT * FROM p{prev};
'''
# P_i (Tuples with minimum _pos for each identifier)
CQL_PI = '''
SELECT MIN(_pos) AS _pos, player_id FROM w{pos}
GROUP BY player_id;
'''
CQL_PI_FINAL = '''
    SELECT {pos} AS _pos, {att} FROM p{pos}, w
    WHERE p{pos}.player_id = w.player_id AND p{pos}._pos = w._pos
    '''


def gen_seq_query(configuration, experiment_conf):
    '''
    Generate SEQ query
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'seq.cql'
    query = SEQ_QUERY.format(ran=experiment_conf[RAN],
                             sli=experiment_conf[SLI])
    write_to_txt(filename, query)


def gen_cql_position_queries(query_dir, experiment_conf):
    '''
    Generate queries to get each position
    '''
    # Generate W_1
    filename = query_dir + os.sep + 'w1.cql'
    write_to_txt(filename, CQL_W1)
    # W_i
    for range_value in range(2, experiment_conf[RAN] + 1):
        query = CQL_WI.format(prev=range_value - 1)
        filename = query_dir + os.sep + \
            'w' + str(range_value) + '.cql'
        write_to_txt(filename, query)
    # P_i
    for range_value in range(1, experiment_conf[RAN] + 1):
        query = CQL_PI.format(pos=range_value)
        filename = query_dir + os.sep + \
            'p' + str(range_value) + '.cql'
        write_to_txt(filename, query)


def gen_cql_w_query(query_dir, experiment_conf):
    '''
    Consider RANGE and SLIDE and generate W relation
    '''
    query = experiment_conf[QUERY]
    if query == Q_MOVE:
        att_list = get_move_attribute_list()
    elif query == Q_PLACE:
        att_list = get_place_attribute_list()
    # Build attribute names list
    att_str = ', '.join(att_list)
    # W
    query = CQL_W.format(att=att_str, ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    filename = query_dir + os.sep + 'w.cql'
    write_to_txt(filename, query)


def gen_cql_equiv_query(query_dir, experiment_conf):
    '''
    Generate final CQL query
    '''
    # Get attribute list
    query = experiment_conf[QUERY]
    if query == Q_MOVE:
        att_list = get_move_attribute_list(prefix='w.')
    elif query == Q_PLACE:
        att_list = get_place_attribute_list(prefix='w.')
    att_str = ', '.join(att_list)
    # List of final position queries
    pos_query_list = []
    for position in range(1, experiment_conf[RAN] + 1):
        pos_query = CQL_PI_FINAL.format(pos=position, att=att_str)
        pos_query_list.append(pos_query)
    # Equivalent is the union of final positions
    query = '\nUNION\n'.join(pos_query_list) + ';'
    filename = query_dir + os.sep + 'equiv.cql'
    write_to_txt(filename, query)


def gen_cql_rpos_spos_queries(query_dir):
    '''
    Generate RPOS and SPOS queries
    '''
    filename = query_dir + os.sep + 'rpos.cql'
    write_to_txt(filename, CQL_RPOS)
    filename = query_dir + os.sep + 'spos.cql'
    write_to_txt(filename, CQL_SPOS)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate all CQL queries
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    gen_cql_rpos_spos_queries(query_dir)
    gen_cql_position_queries(query_dir, experiment_conf)
    gen_cql_w_query(query_dir, experiment_conf)
    gen_cql_equiv_query(query_dir, experiment_conf)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_queries(configuration, exp_conf)
        else:
            gen_seq_query(configuration, exp_conf)


def gen_seq_env(configuration, experiment_conf, output):
    '''
    Generate environment for SEQ
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'seq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='seq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='seq', qfile=filename)
    # Get environment filename
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_cql_env(configuration, experiment_conf, output):
    '''
    Generate environment for CQL
    '''
    text = get_register_stream(experiment_conf)
    query_dir = get_query_dir(configuration, experiment_conf)
    # Environment files for equivalent CQL queries
    # RPOS
    filename = query_dir + os.sep + 'rpos.cql'
    text += REG_Q_STR.format(qname='rpos', qfile=filename)
    # SPOS
    filename = query_dir + os.sep + 'spos.cql'
    text += REG_Q_STR.format(qname='spos', qfile=filename)
    # W
    filename = query_dir + os.sep + 'w.cql'
    text += REG_Q_STR.format(qname='w', qfile=filename)
    # W1 and P1
    filename = query_dir + os.sep + 'w1.cql'
    text += REG_Q_STR.format(qname='w1', qfile=filename)
    filename = query_dir + os.sep + 'p1.cql'
    text += REG_Q_STR.format(qname='p1', qfile=filename)
    # W_i and P_i
    range_value = experiment_conf[RAN]
    for pos in range(2, range_value + 1):
        filename = query_dir + os.sep + 'w' + str(pos) + '.cql'
        text += REG_Q_STR.format(qname='w' + str(pos), qfile=filename)
        filename = query_dir + os.sep + 'p' + str(pos) + '.cql'
        text += REG_Q_STR.format(qname='p' + str(pos), qfile=filename)
    # Final equivalent query
    filename = query_dir + os.sep + 'equiv.cql'
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='equiv', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='equiv', qfile=filename)
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_all_env(configuration, experiment_list, output=False):
    '''
    Generate all environments
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_env(configuration, exp_conf, output)
        else:
            gen_seq_env(configuration, exp_conf, output)
