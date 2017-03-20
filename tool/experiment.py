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

# =============================================================================
# Algorithms
# =============================================================================
# CQL equivalence
CQL_ALG = 'cql'
# SEQ operator
SEQ_ALG = 'seq'
# =============================================================================
# TPref BNL search
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
# Experiment measures
# =============================================================================
# StreamPref measures
RUNTIME = 'runtime'
MEMORY = 'memory'
# Summary measures
SUM_RUN = 'run'
SUM_MEM = 'mem'


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


def get_max_value(parameter_conf, parameter):
    '''
    Return the maximum value of a parameter variation
    '''
    return max(parameter_conf[parameter][VAR])


def get_id(experiment_conf):
    '''
    Return full experiment identifier
    '''
    id_str = ''
    parameter_list = [MATCH, RAN, SLI]
    # For every parameter
    for par in parameter_list:
        # Get value for this parameter in the current experiment
        id_str += par + str(experiment_conf[par])
    return id_str


# def get_data_id(experiment_conf):
#     '''
#     Return experiment identifier for data
#     '''
#     id_str = ''
#     for par in DATA_PAR_LIST:
#         id_str += par + str(experiment_conf[par])
#     return id_str


def get_max_data_timestamp(parameter_conf):
    '''
    Return the maximum timstamp for a generated data stream
    '''
    return max(parameter_conf[RAN][VAR]) + max(parameter_conf[SLI][VAR])


# def get_varied_parameters(parameter_conf):
#     '''
#     Return a list of parameters having variation
#     '''
#     par_list = []
#     for par in parameter_conf:
#         if VAR in parameter_conf[par]:
#             par_list.append(par)
#     return par_list


def get_default_experiment(parameter_conf):
    '''
    Get a experiment with default values for parameters
    '''
    par_list = [par for par in parameter_conf]
    return {par: parameter_conf[par][DEF] for par in par_list}
