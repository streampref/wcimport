# -*- coding: utf-8 -*-
'''
Experiments
'''

# =============================================================================
# Query identifiers
# =============================================================================
Q_PLAY = 'play'
Q_MOVE = 'move'

# =============================================================================
# Experiment parameters
# =============================================================================
# Default value
DEF = 'def'
# Variation
VAR = 'var'

# Range
RAN = 'ran'
# Slide
SLI = 'sli'

# Minimum length of sequences
MIN = 'min'
# Maximum length of sequences
MAX = 'max'

# Query
QUERY = 'q'
# Algorithm
ALGORITHM = 'algo'
# Match
MATCH = 'match'

PARAMETER_VARIATION = [RAN, SLI]

# =============================================================================
# Configuration keys
# =============================================================================
# Algorithm list
ALGORITHM_LIST = 'algo_list'
# Directory
DIRECTORY = 'direc'
# Parameter
PARAMETER = 'dir'
# List of queries
QUERY_LIST = 'query_list'
# List of operators
OPERATOR_LIST = 'operator_list'

# =============================================================================
# Algorithms
# =============================================================================
# CQL equivalence
CQL_ALG = 'cql'
# SEQ operator
SEQ_ALG = 'seq'
# =============================================================================
# BNL search
BNL_SEARCH = 'bnl_search'
# Incremental partition sequence tree
INC_PARTITION_SEQTREE_ALG = 'inc_partition_seqtree'
# Incremental partition sequence tree (with pruning)
INC_PARTITION_SEQTREE_PRUNING_ALG = 'inc_partition_seqtree_pruning'
# Incremental partition list sequence tree
INC_PARTITIONLIST_SEQTREE_ALG = 'inc_partitionlist_seqtree'
# Incremental partition list sequence tree (with pruning)
INC_PARTITIONLIST_SEQTREE_PRUNING_ALG = 'inc_partitionlist_seqtree_pruning'
# =============================================================================
# Algorithms for subsequence operators
NAIVE_SUBSEQ_ALG = "naive"
INC_SUBSEQ_ALG = "incremental"
# =============================================================================
# Algorithms for MINSEQ and MAXSEQ operator
MINSEQ_ALG = "minseq"
MAXSEQ_ALG = "minseq"

# =============================================================================
# Experiment measures
# =============================================================================
# StreamPref measures
RUNTIME = 'runtime'
MEMORY = 'memory'
# Summary measures
SUM_RUN = 'run'
SUM_MEM = 'mem'

# =============================================================================
# Operators
# =============================================================================
SEQ = 'SEQ'
CONSEQ = 'CONSEQ'
ENDSEQ = 'ENDSEQ'
MINSEQ = 'MINSEQ'
MAXSEQ = 'MAXSEQ'
BESTSEQ = 'BESTSEQ'

# =============================================================================
# Query for statistics experiments
# =============================================================================
Q_SEQ = [SEQ]
Q_SEQ_CONSEQ = [SEQ, CONSEQ]
Q_SEQ_ENDSEQ = [SEQ, ENDSEQ]
Q_SEQ_CONSEQ_ENDSEQ = [SEQ, CONSEQ, ENDSEQ]
Q_SEQ_MINSEQ = [SEQ, MINSEQ]
Q_SEQ_MAXSEQ = [SEQ, MAXSEQ]
Q_SEQ_MINSEQ_MAXSEQ = [SEQ, MINSEQ, MAXSEQ]
Q_SEQ_CONSEQ_MINSEQ = [SEQ, CONSEQ, MINSEQ]
Q_SEQ_CONSEQ_MAXSEQ = [SEQ, CONSEQ, MAXSEQ]
Q_SEQ_CONSEQ_MINSEQ_MAXSEQ = [SEQ, CONSEQ, MINSEQ, MAXSEQ]
Q_SEQ_ENDSEQ_MINSEQ = [SEQ, ENDSEQ, MINSEQ]
Q_SEQ_ENDSEQ_MAXSEQ = [SEQ, ENDSEQ, MAXSEQ]
Q_SEQ_ENDSEQ_MINSEQ_MAXSEQ = [SEQ, ENDSEQ, MINSEQ, MAXSEQ]
Q_SEQ_CONSEQ_ENDSEQ_MINSEQ = [SEQ, CONSEQ, ENDSEQ, MINSEQ]
Q_SEQ_CONSEQ_ENDSEQ_MAXSEQ = [SEQ, CONSEQ, ENDSEQ, MAXSEQ]
Q_SEQ_CONSEQ_ENDSEQ_MINSEQ_MAXSEQ = [SEQ, CONSEQ, ENDSEQ, MINSEQ, MAXSEQ]
Q_STATS_LIST = [Q_SEQ, Q_SEQ_CONSEQ, Q_SEQ_ENDSEQ, Q_SEQ_CONSEQ_ENDSEQ,
                Q_SEQ_MINSEQ, Q_SEQ_MAXSEQ, Q_SEQ_MINSEQ_MAXSEQ,
                Q_SEQ_CONSEQ_MINSEQ, Q_SEQ_CONSEQ_MAXSEQ,
                Q_SEQ_CONSEQ_MINSEQ_MAXSEQ, Q_SEQ_ENDSEQ_MINSEQ,
                Q_SEQ_ENDSEQ_MAXSEQ, Q_SEQ_ENDSEQ_MINSEQ_MAXSEQ,
                Q_SEQ_CONSEQ_ENDSEQ_MINSEQ, Q_SEQ_CONSEQ_ENDSEQ_MAXSEQ,
                Q_SEQ_CONSEQ_ENDSEQ_MINSEQ_MAXSEQ]


def add_experiment(experiment_list, experiment):
    '''
    Add an experiment into experiment list
    '''
    if experiment not in experiment_list:
        experiment_list.append(experiment.copy())


def gen_experiment_list(configuration, match_list):
    '''
    Generate the list of experiments
    '''
    exp_list = []
    parameter_conf = configuration[PARAMETER]
    # Default parameters configuration
    def_conf = get_default_experiment(parameter_conf)
    # For every query
    for query in configuration[QUERY_LIST]:
        # For every algorithm
        for alg in configuration[ALGORITHM_LIST]:
            # For every parameter
            for par in parameter_conf:
                # Check if parameter has variation
                if VAR in parameter_conf[par]:
                    # For every value in the variation
                    for value in parameter_conf[par][VAR]:
                        # For every match
                        for match in match_list:
                            # Copy default values
                            conf = def_conf.copy()
                            # Set match
                            conf[MATCH] = match
                            # Set algorithm
                            conf[ALGORITHM] = alg
                            # Set query
                            conf[QUERY] = query
                            # Change parameter to current value
                            conf[par] = value
                            # Add to experiment list
                            add_experiment(exp_list, conf)
    return exp_list


def gen_stats_experiment_list(configuration, match_list):
    '''
    Generate the list of statistical experiments
    '''
    exp_list = []
    parameter_conf = configuration[PARAMETER]
    # Default parameters configuration
    def_conf = get_default_experiment(parameter_conf)
    # For every query
    for query in configuration[QUERY_LIST]:
        # For every algorithm
        for op_list in configuration[OPERATOR_LIST]:
            # For every parameter
            for par in parameter_conf:
                # Check if parameter has variation
                if VAR in parameter_conf[par]:
                    # For every value in the variation
                    for value in parameter_conf[par][VAR]:
                        # For every match
                        for match in match_list:
                            # Copy default values
                            conf = def_conf.copy()
                            # Set match
                            conf[MATCH] = match
                            # Set algorithm
                            conf[OPERATOR_LIST] = op_list
                            # Set query
                            conf[QUERY] = query
                            # Change parameter to current value
                            conf[par] = value
                            # Add to experiment list
                            add_experiment(exp_list, conf)
    return exp_list


def get_max_value(parameter_conf, parameter):
    '''
    Return the maximum value of a parameter variation
    '''
    return max(parameter_conf[parameter][VAR])


def get_id(configuration, experiment_conf):
    '''
    Return full experiment identifier
    '''
    id_str = ''
    par_list = [MATCH]
    par_conf = configuration[PARAMETER]
    for par in par_conf:
        if VAR in par_conf[par]:
            par_list.append(par)
    # For every parameter
    for par in par_list:
        # Get value for this parameter in the current experiment
        id_str += par + str(experiment_conf[par])
    return id_str


def get_max_data_timestamp(parameter_conf):
    '''
    Return the maximum timstamp for a generated data stream
    '''
    return max(parameter_conf[RAN][VAR]) + max(parameter_conf[SLI][VAR])


def get_default_experiment(parameter_conf):
    '''
    Get a experiment with default values for parameters
    '''
    par_list = [par for par in parameter_conf]
    return {par: parameter_conf[par][DEF] for par in par_list}
