#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module for generation of environments for experiments over import data of
soccer world cup of 2014 from http://data.huffingtonpost.com
'''
from tool.experiment import RAN, VAR, DEF, Q_STATS_LIST, OPERATOR_LIST,\
    QUERY_LIST, Q_PLAY, Q_MOVE, DIRECTORY, PARAMETER, MIN, MAX, \
    gen_stats_experiment_list
from tool.io import STATS_MAIN_DIR, get_match_list, create_stat_exp_directories
from tool.query.comp import gen_all_queries, gen_all_env
from tool.run import run_experiments_stats, summarize_all_comp

# =============================================================================
# Experiment execution
# =============================================================================
# Match count
MATCH_COUNT = 1

# Parameters configuration
STATS_PAR = {
    # Range
    RAN: {
        VAR: [60, 120, 180, 240, 300],
        DEF: 180
        },
    # Slide
    #     SLI: {
    #         #         VAR: [1, 5, 15, 60],
    #         DEF: 1
    #         },
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

STATS_CONF = {
    # Algorithms
    OPERATOR_LIST: Q_STATS_LIST,
    # Query
    QUERY_LIST: [Q_PLAY, Q_MOVE],
    # Main directory
    DIRECTORY: STATS_MAIN_DIR,
    # Parameters
    PARAMETER: STATS_PAR
    }


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('STATSGen')
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
    match_list = get_match_list()[-MATCH_COUNT:]
    exp_list = gen_stats_experiment_list(STATS_CONF, match_list)
    if args.gen:
        create_stat_exp_directories(STATS_CONF)
        print 'Generating queries'
        gen_all_queries(STATS_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(STATS_CONF, exp_list)
    elif args.run:
        print 'Running experiments'
        run_experiments_stats(STATS_CONF, exp_list)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all_comp(STATS_CONF, match_list)
#         print 'Calculating confidence intervals'
#         confidence_interval_all(STATS_CONF)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()
