# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

import os

from tool.experiment import QUERY, Q_PLAY, RAN, SLI, Q_MOVE, ALGORITHM, CQL_ALG
from tool.io import get_query_dir, write_to_txt, get_out_file, get_env_file,\
    get_tup_file, write_to_csv, get_aux_out_file
from tool.query.stream import get_register_stream, REG_Q_OUTPUT_STR, REG_Q_STR
from tool.attributes import get_play_attribute_list, get_move_attribute_list,\
    DOM_DICT, TS_ATT, FL_ATT

# =============================================================================
# Queries with preference operators
# =============================================================================
# Play
Q_PLAY_BESTSEQ = '''
SELECT SEQUENCE IDENTIFIED BY pid
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
ACCORDING TO TEMPORAL PREFERENCES
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
SELECT SEQUENCE IDENTIFIED BY pid
[RANGE {ran} SECOND, SLIDE {sli} SECOND] FROM s
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

# =============================================================================
# CQL Equivalences for play query
# =============================================================================
Q_PLAY_DICT = {}
Q_PLAY_ID_LIST = ['z', 'p_join', 'p', 'r1', 'r2', 'nv_ap', 'm_ap', 'r3',
                  'd1_pref', 'd1_npref', 'd2_pref', 'd2_npref',
                  'd3_pref', 'd3_npref', 'd1', 'd2', 'd3', 't1', 't2', 't3',
                  'id', 'equiv']

# Sequence extraction
Q_PLAY_DICT['z'] = '''
SELECT SEQUENCE IDENTIFIED BY pid
[RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Join same positions
Q_PLAY_DICT['p_join'] = '''
SELECT z1._pos, z1.pid AS x1, z1.pc, z1.pl,
                z2.pid AS x2, z2.pc AS _pc, z2.pl AS _pl
FROM z AS z1, z AS z2 WHERE z1._pos =  z2._pos;
'''

# Smaller non correspondent position (positions to be compared)
Q_PLAY_DICT['p'] = '''
SELECT MIN(_pos) AS _pos, x1, x2 FROM p_join
WHERE NOT pc = _pc OR NOT pl = _pl
GROUP BY x1, x2;
'''

# PREVIOUS condition of rule 1
Q_PLAY_DICT['r1'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.pid AND p._pos = z._pos+1 AND z.pl = 're';
'''

# Temporal condition of rule 2
Q_PLAY_DICT['r2'] = '''
SELECT _pos, x1 FROM p;
'''

# ALL PREVIOUS condition of rule 2
Q_PLAY_DICT['nv_ap'] = '''
SELECT MAX(_pos) AS _pos, x1 FROM p GROUP BY x1
UNION
SELECT _pos, pid AS x1 FROM z WHERE NOT pc = 'mf';
'''

Q_PLAY_DICT['m_ap'] = '''
SELECT MIN(_pos) AS _pos, x1 FROM nv_ap GROUP BY x1;
'''

Q_PLAY_DICT['r3'] = '''
SELECT p._pos, p.x1 FROM p, m_ap AS pmin
WHERE p.x1 = pmin.x1 AND p._pos <= pmin._pos AND p._pos > 1;
'''

# Preferred tuples according to rule 1
Q_PLAY_DICT['d1_pref'] = '''
SELECT r._pos, r.x1, pc, pl, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'dr'
UNION
SELECT r._pos, r.x1, t.pc, t.pl, 0 AS t
FROM r1 AS r, tup AS t WHERE t.pl = 'dr';
'''

# Non-preferred tuples according to rule 1
Q_PLAY_DICT['d1_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, pl, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'cp'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.pl, 0 AS t
FROM r1 AS r, tup AS t WHERE t.pl = 'cp';
'''

# Preferred tuples according to rule 2
Q_PLAY_DICT['d2_pref'] = '''
SELECT r._pos, r.x1, pc, pl, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'cp'
UNION
SELECT r._pos, r.x1, t.pc, t.pl, 0 AS t
FROM r2 AS r, tup AS t WHERE t.pl = 'cp';
'''

# Non-preferred tuples according to rule 2
Q_PLAY_DICT['d2_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, pl, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'ncp'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.pl, 0 AS t
FROM r2 AS r, tup AS t WHERE t.pl = 'ncp';
'''

# Preferred tuples according to rule 3
Q_PLAY_DICT['d3_pref'] = '''
SELECT r._pos, r.x1, pc, pl, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'dr'
UNION
SELECT r._pos, r.x1, t.pc, t.pl, 0 AS t
FROM r3 AS r, tup AS t WHERE t.pl = 'dr';
'''

# Non-preferred tuples according to rule 3
Q_PLAY_DICT['d3_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, pl, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND pl = 'cp'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.pl, 0 AS t
FROM r2 AS r, tup AS t WHERE t.pl = 'cp';
'''

# Direct comparisons
Q_PLAY_DICT['d1'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.pl , pref.t,
       npref.pc AS _pc, npref.pl AS _pl, npref.t AS _t
FROM p AS ri, d1_pref AS pref, d1_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2;
'''

Q_PLAY_DICT['d2'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.pl , pref.t,
       npref.pc AS _pc, npref.pl AS _pl, npref.t AS _t
FROM p AS ri, d2_pref AS pref, d2_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.pc = npref.pc;
'''

Q_PLAY_DICT['d3'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.pl , pref.t,
       npref.pc AS _pc, npref.pl AS _pl, npref.t AS _t
FROM p AS ri, d3_pref AS pref, d3_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.pl = npref.pl;
'''

# Transitive comparisons
Q_PLAY_DICT['t1'] = '''
SELECT * FROM d1
UNION SELECT * FROM d2
UNION SELECT * FROM d3;
'''

Q_PLAY_DICT['t2'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.pc, pref.pl, pref.t,
    npref.pc AS _pc, npref.pl AS _pl, npref._t
FROM t1 AS pref, t1 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._pc = npref.pc AND  pref._pl = npref.pl
UNION SELECT * FROM t1;
'''

Q_PLAY_DICT['t3'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.pc, pref.pl, pref.t,
    npref.pc AS _pc, npref.pl AS _pl, npref._t
FROM t2 AS pref, t2 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._pc = npref.pc AND  pref._pl = npref.pl
UNION SELECT * FROM t2;
'''

# ID of dominated sequences
Q_PLAY_DICT['id'] = '''
SELECT DISTINCT pid FROM z
EXCEPT
SELECT DISTINCT x2 AS pid FROM t3
WHERE t = 1 AND _t = 1;
'''

# Dominant sequences
Q_PLAY_DICT['equiv'] = '''
SELECT z.* FROM z, id
WHERE z.pid = id.pid;
'''

# =============================================================================
# CQL Equivalences for move query
# =============================================================================
Q_MOVE_DICT = {}
Q_MOVE_ID_LIST = \
    ['z', 'p_join', 'p', 'r1', 'nv_ap', 'm_ap', 'r2_f1', 'r2_f2', 'r2', 'r3',
     'd1_pref', 'd1_npref', 'd2_pref', 'd2_npref', 'd3_pref', 'd3_npref',
     'd1', 'd2', 'd3', 't1', 't2', 't3', 'id', 'equiv']

# Query for sequence extraction
Q_MOVE_DICT['z'] = '''
SELECT SEQUENCE IDENTIFIED BY pid
[RANGE {ran} SECOND, SLIDE {sli} SECOND]
FROM s;
'''

# Join same positions
Q_MOVE_DICT['p_join'] = '''
SELECT z1._pos, z1.pid AS x1, z1.pc, z1.tb, z1.mv,
    z2.pid AS x2, z2.pc AS _pc, z2.tb AS _tb, z2.mv AS _mv
FROM z AS z1, z AS z2 WHERE z1._pos =  z2._pos;
'''

# Smaller non correspondent position (positions to be compared)
Q_MOVE_DICT['p'] = '''
SELECT MIN(_pos) AS _pos, x1, x2 FROM p_join
WHERE NOT pc = _pc OR NOT tb = _tb OR NOT mv = _mv
GROUP BY x1, x2;
'''

# PREVIOUS condition of rule 1
Q_MOVE_DICT['r1'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.pid AND p._pos = z._pos+1 AND z.pc = 'di';
'''

# ALL PREVIOUS condition of rule 2
Q_MOVE_DICT['nv_ap'] = '''
SELECT MAX(_pos) AS _pos, x1 FROM p GROUP BY x1
UNION
SELECT _pos, pid AS x1 FROM z WHERE NOT tb = 1;
'''

Q_MOVE_DICT['m_ap'] = '''
SELECT MIN(_pos) AS _pos, x1 FROM nv_ap GROUP BY x1;
'''

Q_MOVE_DICT['r2_f1'] = '''
SELECT p._pos, p.x1 FROM p, m_ap AS pmin
WHERE p.x1 = pmin.x1 AND p._pos <= pmin._pos AND p._pos > 1;
'''

# Query equivalent to PREVIOUS condition of rule 2
Q_MOVE_DICT['r2_f2'] = '''
SELECT p._pos, p.x1 FROM z, p
WHERE p.x1 = z.pid AND p._pos = z._pos+1 AND z.pc = 'oi';
'''

# Query equivalent to temporal condition of rule 2
Q_MOVE_DICT['r2'] = '''
SELECT f1._pos, f1.x1 FROM r2_f1 AS f1, r2_f2 AS f2
WHERE f1._pos = f2._pos AND f1.x1 = f2.x1;
'''

# Query equivalent to temporal condition of rule 3
Q_MOVE_DICT['r3'] = '''
SELECT _pos, x1 FROM p;
'''

# Preferred tuples according to rule 1
Q_MOVE_DICT['d1_pref'] = '''
SELECT r._pos, r.x1, pc, tb, mv, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND tb = 1 AND pc = 'mf'
UNION
SELECT r._pos, r.x1, t.pc, t.tb, t.mv, 0 AS t
FROM r1 AS r, tup AS t WHERE t.tb = 1 AND t.pc = 'mf';
'''

# Non-preferred tuples according to rule 1
Q_MOVE_DICT['d1_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, tb, mv, 1 AS t FROM r1 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND tb = 1 AND pc = 'di'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.tb, t.mv, 0 AS t
FROM r1 AS r, tup AS t WHERE t.tb = 1 AND t.pc = 'di';
'''

# Preferred tuples according to rule 2
Q_MOVE_DICT['d2_pref'] = '''
SELECT r._pos, r.x1, pc, tb, mv, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND tb = 0 AND pc = 'mf'
UNION
SELECT r._pos, r.x1, t.pc, t.tb, t.mv, 0 AS t
FROM r2 AS r, tup AS t WHERE t.tb = 0 AND t.pc = 'mf';
'''

# Non-preferred tuples according to rule 2
Q_MOVE_DICT['d2_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, tb, mv, 1 AS t FROM r2 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND tb = 0 AND pc = 'di'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.tb, t.mv, 0 AS t
FROM r2 AS r, tup AS t WHERE t.tb = 0 AND t.pc = 'oi';
'''

# Preferred tuples according to rule 3
Q_MOVE_DICT['d3_pref'] = '''
SELECT r._pos, r.x1, pc, tb, mv, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND mv = 'la'
UNION
SELECT r._pos, r.x1, t.pc, t.tb, t.mv, 0 AS t
FROM r3 AS r, tup AS t WHERE t.mv = 'la';
'''

# Non-preferred tuples according to rule 3
Q_MOVE_DICT['d3_npref'] = '''
SELECT r._pos, r.x1 AS x2, pc, tb, mv, 1 AS t FROM r3 AS r, z
WHERE r._pos = z._pos AND r.x1 = z.pid AND mv = 'fw'
UNION
SELECT r._pos, r.x1 AS x2, t.pc, t.tb, t.mv, 0 AS t
FROM r3 AS r, tup AS t WHERE t.mv = 'fw';
'''

# Direct comparisons
Q_MOVE_DICT['d1'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.tb, pref.mv, pref.t,
       npref.pc AS _pc, npref.tb AS _tb, npref.mv AS _mv, npref.t AS _t
FROM p AS ri, d1_pref AS pref, d1_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2;
'''

Q_MOVE_DICT['d2'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.tb, pref.mv, pref.t,
       npref.pc AS _pc, npref.tb AS _tb, npref.mv AS _mv, npref.t AS _t
FROM p AS ri, d2_pref AS pref, d2_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2 AND pref.mv = npref.mv;
'''

Q_MOVE_DICT['d3'] = '''
SELECT ri._pos, ri.x1, ri.x2, pref.pc, pref.tb, pref.mv, pref.t,
       npref.pc AS _pc, npref.tb AS _tb, npref.mv AS _mv, npref.t AS _t
FROM p AS ri, d3_pref AS pref, d3_npref AS npref
WHERE ri._pos = pref._pos AND ri._pos = npref._pos
AND ri.x1 = pref.x1 AND ri.x2 = npref.x2
AND pref.pc = npref.pc AND pref.tb = npref.tb;
'''

# Transitive comparisons
Q_MOVE_DICT['t1'] = '''
SELECT * FROM d1
UNION SELECT * FROM d2
UNION SELECT * FROM d3;
'''

Q_MOVE_DICT['t2'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.pc, pref.tb, pref.mv, pref.t,
       npref.pc AS _pc, npref.tb AS _tb, npref.mv AS _mv, npref._t
FROM t1 AS pref, t1 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._pc = npref.pc AND pref._tb = npref.tb AND pref._mv = npref.mv
UNION SELECT * FROM t1;
'''

Q_MOVE_DICT['t3'] = '''
SELECT pref._pos, pref.x1, npref.x2, pref.pc, pref.tb, pref.mv, pref.t,
       npref.pc AS _pc, npref.tb AS _tb, npref.mv AS _mv, npref._t
FROM t2 AS pref, t2 AS npref
WHERE pref._pos = npref._pos AND pref.x1 = npref.x1 AND pref.x2 = npref.x2
AND pref._pc = npref.pc AND pref._tb = npref.tb AND pref._mv = npref.mv
UNION SELECT * FROM t2;
'''

# ID of dominant sequences
Q_MOVE_DICT['id'] = '''
SELECT DISTINCT pid FROM z
EXCEPT
SELECT DISTINCT x2 AS pid FROM t3
WHERE t = 1 AND _t = 1;
'''

# Dominant sequences
Q_MOVE_DICT['equiv'] = '''
SELECT z.* FROM z, id
WHERE z.pid = id.pid;
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
    if query == Q_PLAY:
        att_list = get_play_attribute_list()
    elif query == Q_MOVE:
        att_list = get_move_attribute_list()
    rec_list = []
    # Remove PID attribute
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
    Generate streampref queries
    '''
    # Get query dir and filename
    query_dir = get_query_dir(configuration, experiment_conf)
    filename = query_dir + os.sep + 'bestseq.cql'
    # Select correct query
    if experiment_conf[QUERY] == Q_PLAY:
        query = Q_PLAY_BESTSEQ.format(ran=experiment_conf[RAN],
                                    sli=experiment_conf[SLI])
    elif experiment_conf[QUERY] == Q_MOVE:
        query = Q_MOVE_BESTSEQ.format(ran=experiment_conf[RAN],
                                    sli=experiment_conf[SLI])
    # Store query code
    write_to_txt(filename, query)


def gen_cql_queries(configuration, experiment_conf):
    '''
    Generate all queries
    '''
    # Get query dir
    query_dir = get_query_dir(configuration, experiment_conf)
    # Choose correct queries
    if experiment_conf[QUERY] == Q_PLAY:
        query_id_list = Q_PLAY_ID_LIST
        query_dict = Q_PLAY_DICT
        gen_transitive_tuples(Q_PLAY)
    elif experiment_conf[QUERY] == Q_MOVE:
        query_id_list = Q_MOVE_ID_LIST
        query_dict = Q_MOVE_DICT
        gen_transitive_tuples(Q_MOVE)
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
    Generate environment files for SEQ operator
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
    Generate enviroNment files for StremPref
    '''
    # Get register instruction for stream and TUP
    text = get_register_stream(experiment_conf, tup=True)
    # Get query dir
    query_dir = get_query_dir(configuration, experiment_conf)
    # Choose appropriate queries
    if experiment_conf[QUERY] == Q_PLAY:
        query_id_list = Q_PLAY_ID_LIST
    elif experiment_conf[QUERY] == Q_MOVE:
        query_id_list = Q_MOVE_ID_LIST
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
    Generate all environment files
    '''
    for exp_conf in experiment_list:
        if exp_conf[ALGORITHM] == CQL_ALG:
            gen_cql_env(configuration, exp_conf, output)
        else:
            gen_bestseq_env(configuration, exp_conf, output)
