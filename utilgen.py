#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module for statistical experiments with operators
'''
from tool.experiment import RAN, VAR, DEF, Q_UTIL_LIST, OPERATOR_LIST,\
    QUERY_LIST, Q_MOVE, Q_PLACE, DIRECTORY, PARAMETER, MIN, MAX, \
    gen_util_experiment_list, Q_MOVE2
from tool.io import UTIL_MAIN_DIR, create_util_exp_directories,\
    get_match_id_list
from tool.query.util import gen_all_queries, gen_all_env
from tool.run import run_experiments_util, summarize_all_util

# =============================================================================
# Experiment execution
# =============================================================================
# Match count
MATCH_COUNT = 1

# Parameters configuration
UTIL_PAR = {
    # Range
    RAN: {
        VAR: [60, 120, 180, 240, 300],
        DEF: 180
        },
    # Min
    MIN: {
        VAR: [2, 4, 6, 8],
        DEF: 2
        },
    # Max
    MAX: {
        VAR: [8, 10, 12, 14],
        DEF: 14
        }
    }

UTIL_CONF = {
    # Algorithms
    OPERATOR_LIST: Q_UTIL_LIST,
    # Query
    QUERY_LIST: [Q_MOVE, Q_MOVE2, Q_PLACE],
    # Main directory
    DIRECTORY: UTIL_MAIN_DIR,
    # Parameters
    PARAMETER: UTIL_PAR
    }


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('UTILGen')
    parser.add_argument('-g', '--gen', action="store_true",
                        default=False,
                        help='Generate files')
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
    exp_list = gen_util_experiment_list(UTIL_CONF, match_list)
    if args.gen:
        create_util_exp_directories(UTIL_CONF)
        print 'Generating queries'
        gen_all_queries(UTIL_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(UTIL_CONF, exp_list)
    elif args.run:
        print 'Running experiments'
        run_experiments_util(UTIL_CONF, exp_list)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all_util(UTIL_CONF, match_list)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()
