# -*- coding: utf-8 -*-
'''
Routines related to streams
'''
from tool.attributes import get_move_attributes_and_types, \
    get_place_attributes_and_types
from tool.experiment import QUERY, MATCH, Q_MOVE, Q_PLACE, Q_MOVE2
from tool.io import get_move_data_file, get_place_data_file, get_tup_file


# =============================================================================
# Strings for registration in environment file
# =============================================================================
REG_STREAM_STR = "REGISTER STREAM s ({atts}) \nINPUT '{dfile}';"
REG_TUP_STR = "\n\nREGISTER TABLE tup ({atts}) \nINPUT '{dfile}';"
REG_Q_STR = "\n\nREGISTER QUERY {qname} \nINPUT '{qfile}';"
REG_Q_OUTPUT_STR = \
    "\n\nREGISTER QUERY {qname} \nINPUT '{qfile}' \nOUTPUT '{ofile}';"


def get_register_stream(experiment_conf, tup=False):
    '''
    Get register steam string
    '''
    query = experiment_conf[QUERY]
    match = experiment_conf[MATCH]
    # Select correct query
    if query in [Q_MOVE, Q_MOVE2]:
        att_list = get_move_attributes_and_types()
        filename = get_move_data_file(match)
        tup_filename = get_tup_file(query)
    elif query == Q_PLACE:
        att_list = get_place_attributes_and_types()
        filename = get_place_data_file(match)
        tup_filename = get_tup_file(query)
    # Get attribute list
    att_str = ', '.join(att_list)
    # Register stream
    text = REG_STREAM_STR.format(atts=att_str, dfile=filename)
    if tup:
        # Do not consider PID for TUP
        att_list = att_list[1:]
        att_str = ', '.join(att_list)
        text += REG_TUP_STR.format(atts=att_str, dfile=tup_filename)
    text += '\n\n' + '#' * 80 + '\n\n'
    return text
