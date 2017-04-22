#!/usr/bin/python -u
# -*- coding: utf-8 -*-

'''
Module for generation of environments for experiments over import data of
soccer world cup of 2014 from http://data.huffingtonpost.com
'''

from tool.experiment import RAN, VAR, SLI, DEF, CQL_ALG, NAIVE_SUBSEQ_ALG, \
    INC_SUBSEQ_ALG, PARAMETER, QUERY_LIST, Q_PLAY, DIRECTORY, \
    ALGORITHM_LIST, Q_MOVE, gen_experiment_list
from tool.io import CONSEQ_MAIN_DIR, get_match_list, \
    create_experiment_directories
from tool.query.conseq import gen_all_queries, gen_all_env
from tool.run import run_experiments, summarize_all, confidence_interval_all


# =============================================================================
# Experiment execution
# =============================================================================
# Number of experiment runs
RUN_COUNT = 3
# Match count
MATCH_COUNT = 4

# Parameters configuration
CONSEQ_PAR = {
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

CONSEQ_CONF = {
    # Algorithms
    ALGORITHM_LIST: [CQL_ALG, INC_SUBSEQ_ALG, NAIVE_SUBSEQ_ALG],
    # Query
    QUERY_LIST: [Q_PLAY, Q_MOVE],
    # Main directory
    DIRECTORY: CONSEQ_MAIN_DIR,
    # Parameters
    PARAMETER: CONSEQ_PAR
    }


def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('CONSEQGen')
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
    match_list = get_match_list()[-MATCH_COUNT:]
    exp_list = gen_experiment_list(CONSEQ_CONF, match_list)
    if args.gen:
        create_experiment_directories(CONSEQ_CONF, exp_list)
        print 'Generating queries'
        gen_all_queries(CONSEQ_CONF, exp_list)
        print 'Generating environments'
        gen_all_env(CONSEQ_CONF, exp_list, output=args.output)
    elif args.run:
        print 'Running experiments'
        run_experiments(CONSEQ_CONF, exp_list, RUN_COUNT)
    elif args.summarize:
        print 'Summarizing results'
        summarize_all(CONSEQ_CONF, match_list, RUN_COUNT)
        print 'Calculating confidence intervals'
        confidence_interval_all(CONSEQ_CONF)
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()
