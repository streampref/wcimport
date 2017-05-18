#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module for experiments with MINSEQ operator
'''

from tool.experiment import RAN, VAR, SLI, DEF, CQL_ALG, MINSEQ_ALG,\
    PARAMETER, QUERY_LIST, Q_MOVE, DIRECTORY, ALGORITHM_LIST, \
    gen_experiment_list, Q_PLACE, MIN
from tool.io import MINSEQ_MAIN_DIR, get_match_id_list, \
    create_experiment_directories
from tool.query.minseq import gen_all_queries, gen_all_env
from tool.run import run_experiments, summarize_all, confidence_interval_all

# =============================================================================
# Experiment execution
# =============================================================================
# Number of experiment runs
RUN_COUNT = 3
# Match count
MATCH_COUNT = 1

# Parameters configuration
MINSEQ_PAR = {
    # Range
    RAN: {
        VAR: [6, 12, 18, 24, 30],
        DEF: 12
        },
    # Slide
    SLI: {
        VAR: [1, 3, 6, 9, 12],
        DEF: 1
        },
    # Min
    MIN: {
        VAR: [2, 4, 6, 8, 10, 12],
        DEF: 6
        }
    }

MINSEQ_CONF = {
    # Algorithms
    ALGORITHM_LIST: [CQL_ALG, MINSEQ_ALG],
    # Query
    QUERY_LIST: [Q_MOVE, Q_PLACE],
    # Main directory
    DIRECTORY: MINSEQ_MAIN_DIR,
    # Parameters
    PARAMETER: MINSEQ_PAR
    }


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('MINSEQGen')
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
    exp_list = gen_experiment_list(MINSEQ_CONF, match_list)
    if args.gen:
        create_experiment_directories(MINSEQ_CONF, exp_list)
        print 'Generating queries'
        gen_all_queries(MINSEQ_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(MINSEQ_CONF, exp_list, output=args.output)
    elif args.run:
        print 'Running experiments'
        run_experiments(MINSEQ_CONF, exp_list, RUN_COUNT)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all(MINSEQ_CONF, match_list, RUN_COUNT)
        print 'Calculating confidence intervals'
        confidence_interval_all(MINSEQ_CONF)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()
