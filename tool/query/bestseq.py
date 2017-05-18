# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

import os

from tool.experiment import QUERY, Q_MOVE, RAN, SLI, Q_PLACE, ALGORITHM, \
    CQL_ALG
from tool.io import get_query_dir, write_to_txt, get_out_file, get_env_file,\
    get_tup_file, write_to_csv, get_aux_out_file
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR
from tool.attributes import get_move_attribute_list, get_place_attribute_list,\
    DOM_DICT, TS_ATT, FL_ATT

# =============================================================================
# Queries with preference operators
# =============================================================================
# Moves
Q_MOVE_BESTSEQ = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
ACCORDING TO TEMPORAL PREFERENCES
IF PREVIOUS (move = 'rec') THEN
    (move = 'drib') BETTER (move = 'pass') [place]
AND
    (move = 'pass') BETTER (move = 'bpass')
AND
IF ALL PREVIOUS (place = 'mf') THEN
    (place = 'mf') BETTER (place = 'di')
;
'''

# Place
Q_PLACE_BESTSEQ = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
ACCORDING TO TEMPORAL PREFERENCES
IF PREVIOUS (place = 'di') AND (ball = 1) THEN
    (place = 'mf') BETTER (place = 'di')[direc]
AND
IF ALL PREVIOUS (ball = 1) AND (ball = 0) AND PREVIOUS (place = 'oi') THEN
    (place = 'mf') BETTER (place = 'oi')
AND
(direc = 'la') BETTER (direc = 'fw')
;
'''

# =============================================================================
# CQL Equivalences for moves
# =============================================================================
Q_MOVE_DICT = {}
Q_MOVE_ID_LIST = ['z', 'p_join', 'p', 'r1', 'r2', 'nv_ap', 'm_ap', 'r3',
                  'd1_pref', 'd1_npref', 'd2_pref', 'd2_npref',
                  'd3_pref', 'd3_npref', 'd1', 'd2', 'd3', 't1', 't2', 't3',
                  'id', 'equiv']

# Sequence extraction
Q_MOVE_DICT['z'] = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Join same positions
Q_MOVE_DICT['p_join'] = '''
SELECT z1._pos, z1.player_id AS x1, z1.place, z1.move,
                z2.player_id AS x2, z2.place AS _place, z2.move AS _move
FROM z AS z1, z AS z2 WHERE z1._pos =  z2._pos;
'''

# Smaller non correspondent position (positions to be compared)
Q_MOVE_DICT['p'] = '''
SELECT MIN(_pos) AS _pos, x1, x2 FROM p_join
WHERE NOT place = _place OR NOT move = _move
GROUP BY x1, x2;
'''

# PREVIOUS condition of rule 1
Q_MOVE_DICT['r1'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.player_id AND p._pos = z._pos+1 AND z.move = 'rec';
'''

# Temporal condition of rule 2
Q_MOVE_DICT['r2'] = '''
SELECT _pos, x1 FROM p;
'''

# ALL PREVIOUS condition of rule 2
Q_MOVE_DICT['nv_ap'] = '''
SELECT MAX(_pos) AS _pos, x1 FROM p GROUP BY x1
UNION
SELECT _pos, player_id AS x1 FROM z WHERE NOT place = 'mf';
'''

Q_MOVE_DICT['m_ap'] = '''
SELECT MIN(_pos) AS _pos, x1 FROM nv_ap GROUP BY x1;
'''

Q_MOVE_DICT['r3'] = '''
SELECT p._pos, p.x1 FROM p, m_ap AS pmin
WHERE p.x1 = pmin.x1 AND p._pos <= pmin._pos AND p._pos > 1;
'''

# Preferred tuples according to rule 1
Q_MOVE_DICT['d1_pref'] = '''
SELECT r._pos, r.x1, place, move, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'drib'
UNION
SELECT r._pos, r.x1, t.place, t.move, 0 AS t
FROM r1 AS r, tup AS t WHERE t.move = 'drib';
'''

# Non-preferred tuples according to rule 1
Q_MOVE_DICT['d1_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, move, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'pass'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.move, 0 AS t
FROM r1 AS r, tup AS t WHERE t.move = 'pass';
'''

# Preferred tuples according to rule 2
Q_MOVE_DICT['d2_pref'] = '''
SELECT r._pos, r.x1, place, move, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'pass'
UNION
SELECT r._pos, r.x1, t.place, t.move, 0 AS t
FROM r2 AS r, tup AS t WHERE t.move = 'pass';
'''

# Non-preferred tuples according to rule 2
Q_MOVE_DICT['d2_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, move, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'bpass'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.move, 0 AS t
FROM r2 AS r, tup AS t WHERE t.move = 'bpass';
'''

# Preferred tuples according to rule 3
Q_MOVE_DICT['d3_pref'] = '''
SELECT r._pos, r.x1, place, move, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'drib'
UNION
SELECT r._pos, r.x1, t.place, t.move, 0 AS t
FROM r3 AS r, tup AS t WHERE t.move = 'drib';
'''

# Non-preferred tuples according to rule 3
Q_MOVE_DICT['d3_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, move, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'pass'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.move, 0 AS t
FROM r2 AS r, tup AS t WHERE t.move = 'pass';
'''

# Direct comparisons
Q_MOVE_DICT['d1'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.move , pref.t,
       npref.place AS _place, npref.move AS _move, npref.t AS _t
FROM p AS ri, d1_pref AS pref, d1_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2;
'''

Q_MOVE_DICT['d2'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.move , pref.t,
       npref.place AS _place, npref.move AS _move, npref.t AS _t
FROM p AS ri, d2_pref AS pref, d2_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.place = npref.place;
'''

Q_MOVE_DICT['d3'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.move , pref.t,
       npref.place AS _place, npref.move AS _move, npref.t AS _t
FROM p AS ri, d3_pref AS pref, d3_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.move = npref.move;
'''

# Transitive comparisons
Q_MOVE_DICT['t1'] = '''
SELECT * FROM d1
UNION SELECT * FROM d2
UNION SELECT * FROM d3;
'''

Q_MOVE_DICT['t2'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.place, pref.move, pref.t,
    npref.place AS _place, npref.move AS _move, npref._t
FROM t1 AS pref, t1 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._place = npref.place AND  pref._move = npref.move
UNION SELECT * FROM t1;
'''

Q_MOVE_DICT['t3'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.place, pref.move, pref.t,
    npref.place AS _place, npref.move AS _move, npref._t
FROM t2 AS pref, t2 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._place = npref.place AND  pref._move = npref.move
UNION SELECT * FROM t2;
'''

# ID of dominated sequences
Q_MOVE_DICT['id'] = '''
SELECT DISTINCT player_id FROM z
EXCEPT
SELECT DISTINCT x2 AS player_id FROM t3
WHERE t = 1 AND _t = 1;
'''

# Dominant sequences
Q_MOVE_DICT['equiv'] = '''
SELECT z.* FROM z, id
WHERE z.player_id = id.player_id;
'''

# =============================================================================
# CQL Equivalences for place
# =============================================================================
Q_PLACE_DICT = {}
Q_PLACE_ID_LIST = \
    ['z', 'p_join', 'p', 'r1', 'nv_ap', 'm_ap', 'r2_f1', 'r2_f2', 'r2', 'r3',
     'd1_pref', 'd1_npref', 'd2_pref', 'd2_npref', 'd3_pref', 'd3_npref',
     'd1', 'd2', 'd3', 't1', 't2', 't3', 'id', 'equiv']

# Query for sequence extraction
Q_PLACE_DICT['z'] = '''
SELECT SEQUENCE IDENTIFIED BY player_id
[RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Join same positions
Q_PLACE_DICT['p_join'] = '''
SELECT z1._pos, z1.player_id AS x1, z1.place, z1.ball, z1.direc,
    z2.player_id AS x2, z2.place AS _place, z2.ball AS _ball,
    z2.direc AS _direc
FROM z AS z1, z AS z2 WHERE z1._pos =  z2._pos;
'''

# Smaller non correspondent position (positions to be compared)
Q_PLACE_DICT['p'] = '''
SELECT MIN(_pos) AS _pos, x1, x2 FROM p_join
WHERE NOT place = _place OR NOT ball = _ball OR NOT direc = _direc
GROUP BY x1, x2;
'''

# PREVIOUS condition of rule 1
Q_PLACE_DICT['r1'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.player_id AND p._pos = z._pos+1 AND z.place = 'di';
'''

# ALL PREVIOUS condition of rule 2
Q_PLACE_DICT['nv_ap'] = '''
SELECT MAX(_pos) AS _pos, x1 FROM p GROUP BY x1
UNION
SELECT _pos, player_id AS x1 FROM z WHERE NOT ball = 1;
'''

Q_PLACE_DICT['m_ap'] = '''
SELECT MIN(_pos) AS _pos, x1 FROM nv_ap GROUP BY x1;
'''

Q_PLACE_DICT['r2_f1'] = '''
SELECT p._pos, p.x1 FROM p, m_ap AS pmin
WHERE p.x1 = pmin.x1 AND p._pos <= pmin._pos AND p._pos > 1;
'''

# Query equivalent to PREVIOUS condition of rule 2
Q_PLACE_DICT['r2_f2'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.player_id AND p._pos = z._pos+1 AND z.place = 'oi';
'''

# Query equivalent to temporal condition of rule 2
Q_PLACE_DICT['r2'] = '''
SELECT f1._pos, f1.x1 FROM r2_f1 AS f1, r2_f2 AS f2
WHERE f1._pos = f2._pos AND f1.x1 = f2.x1;
'''

# Query equivalent to temporal condition of rule 3
Q_PLACE_DICT['r3'] = '''
SELECT _pos, x1 FROM p;
'''

# Preferred tuples according to rule 1
Q_PLACE_DICT['d1_pref'] = '''
SELECT r._pos, r.x1, place, ball, direc, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND ball = 1 AND place = 'mf'
UNION
SELECT r._pos, r.x1, t.place, t.ball, t.direc, 0 AS t
FROM r1 AS r, tup AS t WHERE t.ball = 1 AND t.place = 'mf';
'''

# Non-preferred tuples according to rule 1
Q_PLACE_DICT['d1_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, ball, direc, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND ball = 1 AND place = 'di'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.ball, t.direc, 0 AS t
FROM r1 AS r, tup AS t WHERE t.ball = 1 AND t.place = 'di';
'''

# Preferred tuples according to rule 2
Q_PLACE_DICT['d2_pref'] = '''
SELECT r._pos, r.x1, place, ball, direc, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND ball = 0 AND place = 'mf'
UNION
SELECT r._pos, r.x1, t.place, t.ball, t.direc, 0 AS t
FROM r2 AS r, tup AS t WHERE t.ball = 0 AND t.place = 'mf';
'''

# Non-preferred tuples according to rule 2
Q_PLACE_DICT['d2_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, ball, direc, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND ball = 0 AND place = 'di'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.ball, t.direc, 0 AS t
FROM r2 AS r, tup AS t WHERE t.ball = 0 AND t.place = 'oi';
'''

# Preferred tuples according to rule 3
Q_PLACE_DICT['d3_pref'] = '''
SELECT r._pos, r.x1, place, ball, direc, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND direc = 'la'
UNION
SELECT r._pos, r.x1, t.place, t.ball, t.direc, 0 AS t
FROM r3 AS r, tup AS t WHERE t.direc = 'la';
'''

# Non-preferred tuples according to rule 3
Q_PLACE_DICT['d3_npref'] = '''
SELECT r._pos, r.x1 AS x2, place, ball, direc, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.player_id AND direc = 'fw'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.ball, t.direc, 0 AS t
FROM r3 AS r, tup AS t WHERE t.direc = 'fw';
'''

# Direct comparisons
Q_PLACE_DICT['d1'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.ball, pref.direc, pref.t,
       npref.place AS _place, npref.ball AS _ball,
        npref.direc AS _direc, npref.t AS _t
FROM p AS ri, d1_pref AS pref, d1_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2;
'''

Q_PLACE_DICT['d2'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.ball, pref.direc, pref.t,
       npref.place AS _place, npref.ball AS _ball,
       npref.direc AS _direc, npref.t AS _t
FROM p AS ri, d2_pref AS pref, d2_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2 AND pref.direc = npref.direc;
'''

Q_PLACE_DICT['d3'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.place, pref.ball, pref.direc, pref.t,
       npref.place AS _place, npref.ball AS _ball,
       npref.direc AS _direc, npref.t AS _t
FROM p AS ri, d3_pref AS pref, d3_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.place = npref.place AND pref.ball = npref.ball;
'''

# Transitive comparisons
Q_PLACE_DICT['t1'] = '''
SELECT * FROM d1
UNION SELECT * FROM d2
UNION SELECT * FROM d3;
'''

Q_PLACE_DICT['t2'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.place, pref.ball, pref.direc,
       pref.t,
       npref.place AS _place, npref.ball AS _ball,
       npref.direc AS _direc, npref._t
FROM t1 AS pref, t1 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._place = npref.place AND pref._ball = npref.ball
AND pref._direc = npref.direc
UNION SELECT * FROM t1;
'''

Q_PLACE_DICT['t3'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.place, pref.ball, pref.direc,
       pref.t,
       npref.place AS _place, npref.ball AS _ball,
       npref.direc AS _direc, npref._t
FROM t2 AS pref, t2 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._place = npref.place AND pref._ball = npref.ball
AND pref._direc = npref.direc
UNION SELECT * FROM t2;
'''

# ID of dominant sequences
Q_PLACE_DICT['id'] = '''
SELECT DISTINCT player_id FROM z
EXCEPT
SELECT DISTINCT x2 AS player_id FROM t3
WHERE t = 1 AND _t = 1;
'''

# Dominant sequences
Q_PLACE_DICT['equiv'] = '''
SELECT z.* FROM z, id
WHERE z.player_id = id.player_id;
'''


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
    if query == Q_MOVE:
        att_list = get_move_attribute_list()
    elif query == Q_PLACE:
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
    if experiment_conf[QUERY] == Q_MOVE:
        query = Q_MOVE_BESTSEQ.format(ran=experiment_conf[RAN],
                                      sli=experiment_conf[SLI])
    elif experiment_conf[QUERY] == Q_PLACE:
        query = Q_PLACE_BESTSEQ.format(ran=experiment_conf[RAN],
                                       sli=experiment_conf[SLI])
    # Store query code
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate CQL queries
    '''
    # Get query dir
    query_dir = get_query_dir(configuration, experiment_conf)
    # Choose correct queries
    if experiment_conf[QUERY] == Q_MOVE:
        query_id_list = Q_MOVE_ID_LIST
        query_dict = Q_MOVE_DICT
        gen_transitive_tuples(Q_MOVE)
    elif experiment_conf[QUERY] == Q_PLACE:
        query_id_list = Q_PLACE_ID_LIST
        query_dict = Q_PLACE_DICT
        gen_transitive_tuples(Q_PLACE)
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
    if experiment_conf[QUERY] == Q_MOVE:
        query_id_list = Q_MOVE_ID_LIST
    elif experiment_conf[QUERY] == Q_PLACE:
        query_id_list = Q_PLACE_ID_LIST
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
