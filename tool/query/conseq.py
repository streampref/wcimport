# -*- coding: utf-8 -*-
'''
Queries for experiments with CONSEQ operator
'''

import os

from tool.attributes import get_move_attribute_list, get_place_attribute_list
from tool.experiment import SLI, RAN, ALGORITHM, \
    CQL_ALG, QUERY, Q_MOVE, Q_PLACE
from tool.io import get_query_dir, write_to_txt, get_out_file, get_env_file
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR


# =============================================================================
# Query using CONSEQ operator
# =============================================================================
CONSEQ_QUERY = '''
SELECT SUBSEQUENCE CONSECUTIVE TIMESTAMP
FROM SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s;
'''

# =============================================================================
# CQL Equivalent Queries
# =============================================================================
# Original timestamp of tuples in original TS attribute
CQL_TABLE_OTS = '''
SELECT _ts AS ots, * FROM s[NOW];
'''

# Transform table with original TS into stream
CQL_STREAM_OTS = '''
SELECT RSTREAM FROM table_ots;
'''

# Query to get sequence from stream with OTS
CQL_Z = '''
SELECT SEQUENCE IDENTIFIED BY player_id
    [RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM stream_ots;
'''

# Auxiliar query to compare timestamps
CQL_Z_PRIME = '''
SELECT _pos + 1 AS _pos, ots + 1 AS ots, player_id FROM z;
'''

# Start position of ct-subsequences
CQL_P_START = '''
SELECT _pos AS start, z.player_id FROM z
WHERE _pos = 1
UNION
SELECT z._pos AS start, z.player_id
FROM z, z_prime AS zp
WHERE z._pos = zp._pos AND z.player_id = zp.player_id
AND NOT z.ots = zp.ots;
'''

# End position of ct-subsequences
CQL_P_END = '''
SELECT start - 1 AS end, player_id FROM p_start
WHERE start > 1
UNION
SELECT MAX(z._pos) AS end, player_id FROM z
GROUP BY player_id;
'''

# Start and end of ct-subsequences
CQL_P_START_END = '''
SELECT start, MIN(end) AS end, s.player_id
FROM p_start AS s, p_end AS e
WHERE s.player_id = e.player_id AND start <= end
GROUP BY start, s.player_id;
'''

# Query equivalent to CONSEQ operator
CQL_EQUIV = '''
SELECT z._pos - se.start + 1 AS _pos, {zatt}
FROM z, p_start_end AS se
WHERE z.player_id = se.player_id
AND z._pos >= se.start AND z._pos <= se.end;
    '''


def gen_conseq_query(configuration, experiment_conf):
    '''
    Generate queries with CONSEQ operator
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'conseq.cql'
    query = CONSEQ_QUERY.format(ran=experiment_conf[RAN],
                                sli=experiment_conf[SLI])
    write_to_txt(filename, query)


def gen_cql_z_query(query_dir, experiment_conf):
    '''
    Consider RANGE and SLIDE and generate Z relation
    '''
    query = CQL_Z.format(ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    filename = query_dir + os.sep + 'z.cql'
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate CQL queries
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'table_ots.cql'
    write_to_txt(filename, CQL_TABLE_OTS)
    filename = query_dir + os.sep + 'stream_ots.cql'
    write_to_txt(filename, CQL_STREAM_OTS)
    gen_cql_z_query(query_dir, experiment_conf)
    filename = query_dir + os.sep + 'z_prime.cql'
    write_to_txt(filename, CQL_Z_PRIME)
    filename = query_dir + os.sep + 'p_start.cql'
    write_to_txt(filename, CQL_P_START)
    filename = query_dir + os.sep + 'p_end.cql'
    write_to_txt(filename, CQL_P_END)
    filename = query_dir + os.sep + 'p_start_end.cql'
    write_to_txt(filename, CQL_P_START_END)
    filename = query_dir + os.sep + 'equiv.cql'
    if experiment_conf[QUERY] == Q_MOVE:
        att_list = get_move_attribute_list('z.')
    elif experiment_conf[QUERY] == Q_PLACE:
        att_list = get_place_attribute_list('z.')
    att_list = ', '.join(att_list)
    query = CQL_EQUIV.format(zatt=att_list)
    write_to_txt(filename, query)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_queries(configuration, exp_conf)
        else:
            gen_conseq_query(configuration, exp_conf)


def gen_conseq_env(configuration, experiment_conf, output):
    '''
    Generate environment for CONSEQ
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'conseq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='conseq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='conseq', qfile=filename)
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
    filename = query_dir + os.sep + 'table_ots.cql'
    text += REG_Q_STR.format(qname='table_ots', qfile=filename)
    filename = query_dir + os.sep + 'stream_ots.cql'
    text += REG_Q_STR.format(qname='stream_ots', qfile=filename)
    filename = query_dir + os.sep + 'z.cql'
    text += REG_Q_STR.format(qname='z', qfile=filename)
    filename = query_dir + os.sep + 'z_prime.cql'
    text += REG_Q_STR.format(qname='z_prime', qfile=filename)
    filename = query_dir + os.sep + 'p_start.cql'
    text += REG_Q_STR.format(qname='p_start', qfile=filename)
    filename = query_dir + os.sep + 'p_end.cql'
    text += REG_Q_STR.format(qname='p_end', qfile=filename)
    filename = query_dir + os.sep + 'p_start_end.cql'
    text += REG_Q_STR.format(qname='p_start_end', qfile=filename)
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
            gen_conseq_env(configuration, exp_conf, output)
