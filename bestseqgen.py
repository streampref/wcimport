#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module for experiments with BESTSEQ operator
'''

from tool.experiment import RAN, VAR, SLI, DEF, CQL_ALG, \
    PARAMETER, QUERY_LIST, Q_MOVE, DIRECTORY, ALGORITHM_LIST, \
    gen_experiment_list, Q_PLACE, BNL_SEARCH, INC_PARTITION_SEQTREE_ALG,\
    INC_PARTITION_SEQTREE_PRUNING_ALG, INC_PARTITIONLIST_SEQTREE_ALG,\
    INC_PARTITIONLIST_SEQTREE_PRUNING_ALG, Q_MOVE2
from tool.io import BESTSEQ_MAIN_DIR, \
    create_experiment_directories, get_match_id_list
from tool.run import run_experiments, summarize_all, confidence_interval_all
from tool.query.bestseq.base import gen_all_queries, gen_all_env

# =============================================================================
# Experiment execution
# =============================================================================
# Number of experiment runs
RUN_COUNT = 3
# Match count
MATCH_COUNT = 1

# Parameters configuration
BESTSEQ_PAR = {
    # Range
    RAN: {
        VAR: [6, 12, 18, 24, 30],
        DEF: 12
        },
    # Slide
    SLI: {
        VAR: [1, 3, 6, 9, 12],
        DEF: 1
        }
    }

BESTSEQ_CONF = {
    # Algorithms
    ALGORITHM_LIST: [CQL_ALG, BNL_SEARCH, INC_PARTITION_SEQTREE_ALG,
                     INC_PARTITION_SEQTREE_PRUNING_ALG,
                     INC_PARTITIONLIST_SEQTREE_ALG,
                     INC_PARTITIONLIST_SEQTREE_PRUNING_ALG],
    # Query
    QUERY_LIST: [Q_MOVE, Q_MOVE2, Q_PLACE],
    # Main directory
    DIRECTORY: BESTSEQ_MAIN_DIR,
    # Parameters
    PARAMETER: BESTSEQ_PAR
    }


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('BESTSEQGen')
    parser.add_argument('-g', '--gen', action="store_true",
                        default=False,
                        help='Generate files')
    parser.add_argument('-o', '--output', action="store_true",
                        default=False,
                        help='Generate query output')
    parser.add_argument('-r', '--run', action="store_true",
                        default=False,
                        help='Run experiments')
    parser.add_argument('-s', '--summarize', action="store_true",
                        default=False,
                        help='Summarize results')
    args = parser.parse_args()
    if print_help:
        parser.print_help()
    return args


def main():
    '''
    Main routine
    '''
    args = get_arguments()
    print 'Getting list of matches'
    match_list = get_match_id_list()[-MATCH_COUNT:]
    exp_list = gen_experiment_list(BESTSEQ_CONF, match_list)
    if args.gen:
        create_experiment_directories(BESTSEQ_CONF, exp_list)
        print 'Generating queries'
        gen_all_queries(BESTSEQ_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(BESTSEQ_CONF, exp_list, output=args.output)
    elif args.run:
        print 'Running experiments'
        run_experiments(BESTSEQ_CONF, exp_list, RUN_COUNT)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all(BESTSEQ_CONF, match_list, RUN_COUNT)
        print 'Calculating confidence intervals'
        confidence_interval_all(BESTSEQ_CONF)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()
