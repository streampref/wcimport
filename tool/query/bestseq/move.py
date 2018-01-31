# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

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
    (move = 'pass') BETTER (move = 'bpas')
AND
IF ALL PREVIOUS (place = 'mf') THEN
    (place = 'mf') BETTER (place = 'di')
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
WHERE r._pos = z._pos AND r.x1 = z.player_id AND move = 'bpas'
UNION
SELECT r._pos, r.x1 AS x2, t.place, t.move, 0 AS t
FROM r2 AS r, tup AS t WHERE t.move = 'bpas';
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
FROM r3 AS r, tup AS t WHERE t.move = 'pass';
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
