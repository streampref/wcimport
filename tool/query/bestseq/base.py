# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

import os

from tool.experiment import QUERY, RAN, SLI, ALGORITHM, \
    CQL_ALG, Q_MOVE2, Q_MOVE, Q_PLACE
from tool.io import get_query_dir, write_to_txt, get_out_file, get_env_file,\
    get_tup_file, write_to_csv, get_aux_out_file
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR
from tool.attributes import get_move_attribute_list, get_place_attribute_list,\
    DOM_DICT, TS_ATT, FL_ATT
from tool.query.bestseq.move import Q_MOVE_BESTSEQ, Q_MOVE_ID_LIST, Q_MOVE_DICT
from tool.query.bestseq.move2 import Q_MOVE2_BESTSEQ, Q_MOVE2_ID_LIST,\
    Q_MOVE2_DICT
from tool.query.bestseq.place import Q_PLACE_BESTSEQ, Q_PLACE_ID_LIST,\
    Q_PLACE_DICT

Q_MOVE_LIST = [Q_MOVE, Q_MOVE2]
Q_PLACE_LIST = [Q_PLACE]


def _combine_records(record_list, attribute, value_list):
    '''
    Combine record list with value list for an attribute
    '''
    # Check if record list is empty
    if len(record_list) == 0:
        return [{attribute: value} for value in value_list]
    # new list of record
    new_rec_list = []
    # For every record
    for rec in record_list:
        # For every value
        for value in value_list:
            # Combine record and value
            new_rec = rec.copy()
            new_rec[attribute] = value
            new_rec_list.append(new_rec)
    return new_rec_list


def gen_transitive_tuples(query):
    '''
    Generate transitive tuples
    '''
    if query in Q_MOVE_LIST:
        att_list = get_move_attribute_list()
    elif query in Q_PLACE_LIST:
        att_list = get_place_attribute_list()
    rec_list = []
    # Remove player_id attribute
    att_list = att_list[1:]
    for att in att_list:
        value_list = DOM_DICT[att]
        rec_list = _combine_records(rec_list, att, value_list)
    for rec in rec_list:
        rec[TS_ATT] = 0
        rec[FL_ATT] = '+'
    filename = get_tup_file(query)
    att_list = [TS_ATT, FL_ATT] + att_list
    write_to_csv(filename, att_list, rec_list)


def gen_bestseq_query(configuration, experiment_conf):
    '''
    Generate BESTSEQ query
    '''
    # Get query dir and filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'bestseq.cql'
    # Select correct query
    query = get_query(experiment_conf[QUERY])
    query = query.format(ran=experiment_conf[RAN],
                         sli=experiment_conf[SLI])
    # Store query code
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate CQL queries
    '''
    # Get query dir
    query_dir = get_query_dir(configuration, experiment_conf)
    query_id_list = get_cql_query_id_list(experiment_conf[QUERY])
    query_dict = get_cql_query_dict(experiment_conf[QUERY])
    gen_transitive_tuples(experiment_conf[QUERY])
    # Store query codes
    for query_id in query_id_list:
        filename = query_dir + os.sep + query_id + '.cql'
        query = query_dict[query_id]
        if query_id == 'z':
            query = \
                query.format(ran=experiment_conf[RAN],
                             sli=experiment_conf[SLI])
        write_to_txt(filename, query)


def gen_all_queries(configuration, experiment_list):
    '''
    Generate all queries
    '''
    # For every experiment
    for exp_conf in experiment_list:
        # Generate appropriate queries
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_queries(configuration, exp_conf)
        else:
            gen_bestseq_query(configuration, exp_conf)


def gen_bestseq_env(configuration, experiment_conf, output):
    '''
    Generate environment for BESTSEQ
    '''
    text = get_register_stream(experiment_conf)
    # Get query filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'bestseq.cql'
    # Register query
    if output:
        # Get output filename
        out_file = get_out_file(configuration, experiment_conf)
        text += REG_Q_OUTPUT_STR.format(qname='bestseq', qfile=filename,
                                        ofile=out_file)
    else:
        text += REG_Q_STR.format(qname='bestseq', qfile=filename)
    # Get environment filename
    filename = get_env_file(configuration, experiment_conf)
    write_to_txt(filename, text)


def gen_cql_env(configuration, experiment_conf, output):
    '''
    Generate environment for CQL
    '''
    # Get register instruction for stream and TUP
    text = get_register_stream(experiment_conf, tup=True)
    # Get query dir
    query_dir = get_query_dir(configuration, experiment_conf)
    # Choose appropriate queries
    query_id_list = get_cql_query_id_list(experiment_conf[QUERY])
    # Register all queries (excet "equiv" query)
    for query_id in query_id_list[:len(query_id_list) - 1]:
        filename = query_dir + os.sep + query_id + '.cql'
        if output:
            out_file = get_aux_out_file(configuration, experiment_conf,
                                        query_id)
            text += REG_Q_OUTPUT_STR.format(qname=query_id, qfile=filename,
                                            ofile=out_file)
        else:
            text += REG_Q_STR.format(qname=query_id, qfile=filename)
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
            gen_bestseq_env(configuration, exp_conf, output)


def get_query(query_id):
    '''
    Get full query code for a query identifier
    '''
    if query_id == Q_MOVE:
        return Q_MOVE_BESTSEQ
    elif query_id == Q_MOVE2:
        return Q_MOVE2_BESTSEQ
    elif query_id == Q_PLACE:
        return Q_PLACE_BESTSEQ


def get_cql_query_id_list(query_id):
    '''
    Get CQL query identifiers
    '''
    if query_id == Q_MOVE:
        return Q_MOVE_ID_LIST
    elif query_id == Q_MOVE2:
        return Q_MOVE2_ID_LIST
    elif query_id == Q_PLACE:
        return Q_PLACE_ID_LIST


def get_cql_query_dict(query_id):
    '''
    Get CQL query dictionaries
    '''
    if query_id == Q_MOVE:
        return Q_MOVE_DICT
    elif query_id == Q_MOVE2:
        return Q_MOVE2_DICT
    elif query_id == Q_PLACE:
        return Q_PLACE_DICT
