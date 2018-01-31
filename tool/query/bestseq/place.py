# -*- coding: utf-8 -*-
'''
Queries for experiments with preference operators
'''

# =============================================================================
# Query with preference operators
# =============================================================================
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
