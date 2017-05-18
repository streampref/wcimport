# -*- coding: utf-8 -*-
'''
Queries for experiments with MINSEQ operator
'''

import os

from tool.io import write_to_txt, get_env_file, get_query_dir, \
    get_out_file
from tool.experiment import SLI, RAN, MIN, ALGORITHM, CQL_ALG
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR


# =============================================================================
# Query using MINSEQ operator
# =============================================================================
MINSEQ_QUERY = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
WHERE MINIMUM LENGTH IS {min}
;
'''

# =============================================================================
# CQL Queries
# =============================================================================
# Query to get sequence from stream
CQL_Z = '''
SELECT SEQUENCE IDENTIFIED BY player_id
    [RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Query to get sequence id having a minium of positions
CQL_ZMIN = '''
SELECT DISTINCT player_id FROM z WHERE _pos >= {min};
'''

# Query equivalent to MINSEQ operator
CQL_EQUIV = '''
SELECT z.* FROM z, zmin WHERE z.player_id = zmin.player_id;
'''


def gen_minseq_query(configuration, experiment_conf):
    '''
    Generate MINSEQ query
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'minseq.cql'
    query = MINSEQ_QUERY.format(min=experiment_conf[MIN],
                                ran=experiment_conf[RAN],
                                sli=experiment_conf[SLI])
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate CQL queries
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    query = CQL_Z.format(ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    filename = query_dir + os.sep + 'z.cql'
    write_to_txt(filename, query)
    query = CQL_ZMIN.format(min=experiment_conf[MIN])
    filename = query_dir + os.sep + 'zmin.cql'
    write_to_txt(filename, query)
    filename = query_dir + os.sep + 'equiv.cql'
    write_to_txt(filename, CQL_EQUIV)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_queries(configuration, exp_conf)
        else:
            gen_minseq_query(configuration, exp_conf)


def gen_minseq_env(configuration, experiment_conf, output):
    '''
    Generate environment for MINSEQ
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'minseq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='minseq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='minseq', qfile=filename)
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
    filename = query_dir + os.sep + 'z.cql'
    text += REG_Q_STR.format(qname='z', qfile=filename)
    filename = query_dir + os.sep + 'zmin.cql'
    text += REG_Q_STR.format(qname='zmin', qfile=filename)
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
            gen_minseq_env(configuration, exp_conf, output)
