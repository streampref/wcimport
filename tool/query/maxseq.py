# -*- coding: utf-8 -*-
'''
Queries for experiments with MAXSEQ operator
'''

import os

from tool.io import write_to_txt, get_env_file, get_query_dir, \
    get_out_file
from tool.experiment import SLI, RAN, MAX, ALGORITHM, CQL_ALG
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR


# =============================================================================
# Query using MAXSEQ operator
# =============================================================================
MAXSEQ_QUERY = '''
SELECT SEQUENCE IDENTIFIED BY pid
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
WHERE MAXIMUM LENGTH IS {max}
;
'''

# =============================================================================
# CQL Queries
# =============================================================================
# Query to get sequence from stream
CQL_Z = '''
SELECT SEQUENCE IDENTIFIED BY pid [RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Query to get sequence id having a maxium of positions
CQL_ZMAX = '''
SELECT DISTINCT pid FROM z
EXCEPT
SELECT pid FROM z WHERE _pos > {max};
'''

# Query equivalent to MAXSEQ operator
CQL_EQUIV = '''
SELECT z.* FROM z, zmax WHERE z.pid = zmax.pid;
'''


def gen_maxseq_query(configuration, experiment_conf):
    '''
    Generate queries with MAXSEQ operator
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'maxseq.cql'
    query = MAXSEQ_QUERY.format(max=experiment_conf[MAX],
                                ran=experiment_conf[RAN],
                                sli=experiment_conf[SLI])
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate all CQL queries equivalent to MAXSEQ operator
    '''
    query_dir = get_query_dir(configuration, experiment_conf)
    query = CQL_Z.format(ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    filename = query_dir + os.sep + 'z.cql'
    write_to_txt(filename, query)
    query = CQL_ZMAX.format(max=experiment_conf[MAX])
    filename = query_dir + os.sep + 'zmax.cql'
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
            gen_maxseq_query(configuration, exp_conf)


def gen_maxseq_env(configuration, experiment_conf, output):
    '''
    Generate environment files for MAXSEQ operator
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'maxseq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='maxseq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='maxseq', qfile=filename)
    # Get environment filename
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_cql_env(configuration, experiment_conf, output):
    '''
    Generate environment files for StremPref
    '''
    text = get_register_stream(configuration, experiment_conf)
    query_dir = get_query_dir(configuration, experiment_conf)
    # Environment files for equivalent CQL queries
    filename = query_dir + os.sep + 'z.cql'
    text += REG_Q_STR.format(qname='z', qfile=filename)
    filename = query_dir + os.sep + 'zmax.cql'
    text += REG_Q_STR.format(qname='zmax', qfile=filename)
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
    Generate all environment files
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_env(configuration, exp_conf, output)
        else:
            gen_maxseq_env(configuration, exp_conf, output)
