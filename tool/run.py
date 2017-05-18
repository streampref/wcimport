# -*- coding: utf-8 -*-
'''
Experiments execution
'''

import csv
import os

from tool.io import get_detail_file, get_env_file, write_result_file, \
    get_summary_file, get_result_file, get_max_move_ts, get_max_place_ts,\
    get_env_stats_file, get_detail_stats_file
from tool.experiment import ALGORITHM, PARAMETER, VAR, CQL_ALG, \
    SEQ_ALG, RUNTIME, MEMORY, SUM_RUN, SUM_MEM, BNL_SEARCH, \
    INC_PARTITION_SEQTREE_ALG, INC_PARTITIONLIST_SEQTREE_ALG, \
    INC_PARTITION_SEQTREE_PRUNING_ALG, INC_PARTITIONLIST_SEQTREE_PRUNING_ALG, \
    get_default_experiment, MATCH, QUERY, QUERY_LIST,\
    Q_MOVE, Q_PLACE, ALGORITHM_LIST, NAIVE_SUBSEQ_ALG, INC_SUBSEQ_ALG, \
    MINSEQ_ALG, MAXSEQ_ALG, get_variated_parameters, OPERATOR_LIST,\
    STATS_ATT_LIST, STATS_IN


# Command for experiment run
SIMPLE_RUN_COMMAND = "streampref -r'|' -e {env} -d {det} -m {max}"
# Command for experiment run with temporal preference algorithm option
BESTSEQ_RUN_COMMAND = "streampref -r'|' -e {env} -d {det} -m {max} -t {alg}"
# Command for experiment run with subsequence algorithm option
SUBSEQ_RUN_COMMAND = "streampref -r'|' -e {env} -d {det} -m {max} -s {alg}"
# Command for experiment run with statistics output
STATS_RUN_COMMAND = "streampref -r'|' -e {env} -o {det} -m {max}"
# Command for calculation of confidence interval
CONFINTERVAL_COMMAND = "confinterval -d'|' -i {inf} -o {outf} -k {keyf}"

# Dictionary of run commands
RUN_DICT = {}
RUN_DICT[CQL_ALG] = SIMPLE_RUN_COMMAND
RUN_DICT[SEQ_ALG] = SIMPLE_RUN_COMMAND
RUN_DICT[BNL_SEARCH] = SIMPLE_RUN_COMMAND
RUN_DICT[INC_PARTITION_SEQTREE_ALG] = BESTSEQ_RUN_COMMAND
RUN_DICT[INC_PARTITIONLIST_SEQTREE_ALG] = BESTSEQ_RUN_COMMAND
RUN_DICT[INC_PARTITION_SEQTREE_PRUNING_ALG] = BESTSEQ_RUN_COMMAND
RUN_DICT[INC_PARTITIONLIST_SEQTREE_PRUNING_ALG] = BESTSEQ_RUN_COMMAND
# Subsequence run commands
RUN_DICT[NAIVE_SUBSEQ_ALG] = SUBSEQ_RUN_COMMAND
RUN_DICT[INC_SUBSEQ_ALG] = SUBSEQ_RUN_COMMAND
# Filter by length run commands
RUN_DICT[MINSEQ_ALG] = SIMPLE_RUN_COMMAND
RUN_DICT[MAXSEQ_ALG] = SIMPLE_RUN_COMMAND


def get_iterations(experiment_conf):
    '''
    Return the number of iterations
    '''
    if experiment_conf[QUERY] == Q_MOVE:
        return get_max_move_ts(experiment_conf[MATCH])
    elif experiment_conf[QUERY] == Q_PLACE:
        return get_max_place_ts(experiment_conf[MATCH])


def run(configuration, experiment_conf, count):
    '''
    Run an experiment
    '''
    # Get iteration number
    iterations = get_iterations(experiment_conf)
    # Get environment file
    env_file = get_env_file(configuration, experiment_conf)
    # Get detail file
    detail_file = get_detail_file(configuration, experiment_conf, count)
    if not os.path.isfile(detail_file):
        command = RUN_DICT[experiment_conf[ALGORITHM]]
        if command == SIMPLE_RUN_COMMAND:
            command = command.format(env=env_file, det=detail_file,
                                     max=iterations)
        elif command in [BESTSEQ_RUN_COMMAND, SUBSEQ_RUN_COMMAND]:
            command = command.format(env=env_file, det=detail_file,
                                     max=iterations,
                                     alg=experiment_conf[ALGORITHM])
        print command
        os.system(command)
        if not os.path.isfile(detail_file):
            print 'Detail results file not found: ' + detail_file
            print "Check if 'streampref' is in path"


def run_stats(configuration, experiment_conf):
    '''
    Run statistical experiment
    '''
    # Get iteration number
    iterations = get_iterations(experiment_conf)
    # Get environment file
    env_file = get_env_stats_file(configuration, experiment_conf)
    detail_file = get_detail_stats_file(configuration, experiment_conf)
    detail_tmp = detail_file + '.tmp'
    if not os.path.isfile(detail_file):
        command = STATS_RUN_COMMAND.format(env=env_file, det=detail_tmp,
                                           max=iterations)
        print command
        os.system(command)
        os.rename(detail_tmp, detail_file)
        if not os.path.isfile(detail_file):
            print 'Detail results file not found: ' + detail_file
            print "Check if 'streampref' is in path"


def run_experiments(configuration, experiment_list, run_count):
    '''
    Run all experiments
    '''
    for count in range(1, run_count + 1):
        for exp_conf in experiment_list:
            run(configuration, exp_conf, count)


def run_experiments_stats(configuration, experiment_list):
    '''
    Run all experiments with statistics output
    '''
    for exp_conf in experiment_list:
        run_stats(configuration, exp_conf)


def get_summaries(detail_file):
    '''
    Read results from a detail file
    '''
    # Check if file exists
    if not os.path.isfile(detail_file):
        print 'File does not exists: ' + detail_file
        return (float('NaN'), float('NaN'))
    in_file = open(detail_file, 'r')
    reader = csv.DictReader(in_file, skipinitialspace=True)
    sum_time = 0.0
    sum_memory = 0.0
    count = 0
    for rec in reader:
        sum_time += float(rec[RUNTIME])
        sum_memory += float(rec[MEMORY])
        count += 1
    in_file.close()
    # Return total runtime and memory average
    return (sum_time, sum_memory / count)


def get_stats_summaries(detail_file):
    '''
    Read statistical results from a detail file
    '''
    # Check if file exists
    if not os.path.isfile(detail_file):
        print 'File does not exists: ' + detail_file
        return {att: float('NaN') for att in STATS_ATT_LIST}
    rec_out = {att: 0.0 for att in STATS_ATT_LIST}
    in_file = open(detail_file, 'r')
    reader = csv.DictReader(in_file, skipinitialspace=True)
    count = 0
    for rec in reader:
        if rec[STATS_IN] > 0:
            for att in STATS_ATT_LIST:
                rec_out[att] += float(rec[att])
        count += 1
    in_file.close()
    for att in STATS_ATT_LIST:
        rec_out[att] /= count
    return rec_out


def get_match_stats_summaries(configuration, match_list, exp_conf):
    '''
    Get math statistical summaries
    '''
    rec_out = {att: 0.0 for att in STATS_ATT_LIST}
    for match in match_list:
        exp_copy = exp_conf.copy()
        exp_copy[MATCH] = match
        dfile = get_detail_stats_file(configuration, exp_copy)
        rec = get_stats_summaries(dfile)
        for att in STATS_ATT_LIST:
            rec_out[att] += rec[att]
    for att in STATS_ATT_LIST:
        rec_out[att] = rec_out[att] / len(match_list)
    return rec_out


def get_match_summaries(configuration, match_list, exp_conf, count):
    '''
    Get math summaries
    '''
    time_sum = 0.0
    mem_sum = 0.0
    for match in match_list:
        exp_copy = exp_conf.copy()
        exp_copy[MATCH] = match
        dfile = get_detail_file(configuration, exp_copy, count)
        match_time, match_memory = get_summaries(dfile)
        time_sum += match_time
        mem_sum += match_memory
    return time_sum/len(match_list), mem_sum/len(match_list)


def summarize(configuration, match_list, query, parameter, run_count):
    '''
    Summarize experiments
    '''
    # Result lists
    time_list = []
    mem_list = []
    # Get parameter configurations
    par_conf = configuration[PARAMETER]
    # Get default parameter values
    exp_conf = get_default_experiment(par_conf)
    exp_conf[QUERY] = query
    # For every value of current attributes
    for value in par_conf[parameter][VAR]:
        # Get experiment configuration for current value
        exp_conf[parameter] = value
        # For every execution
        for count in range(1, run_count + 1):
            # Creates record for current parameter and value
            time_rec = {parameter: value}
            mem_rec = {parameter: value}
            # For every algorithm
            for alg in configuration[ALGORITHM_LIST]:
                exp_conf[ALGORITHM] = alg
                # Get summarized results
                time_rec[alg], mem_rec[alg] = \
                    get_match_summaries(configuration, match_list,
                                        exp_conf, count)
            # Append to result lists
            time_list.append(time_rec)
            mem_list.append(mem_rec)
    # Store summarized results
    filename = get_summary_file(configuration, query, SUM_RUN, parameter)
    write_result_file(filename, time_list, parameter)
    filename = get_summary_file(configuration, query, SUM_MEM, parameter)
    write_result_file(filename, mem_list, parameter)


def summarize_stats(configuration, match_list, query, parameter):
    '''
    Summarize statistical experiments
    '''
    # Result lists
    rec_list = []
    # Get parameter configurations
    par_conf = configuration[PARAMETER]
    # Get default parameter values
    exp_conf = get_default_experiment(par_conf)
    exp_conf[QUERY] = query
    # For every value of current attributes
    for value in par_conf[parameter][VAR]:
        rec = {parameter: value}
        # Get experiment configuration for current value
        exp_conf[parameter] = value
        for op_list in configuration[OPERATOR_LIST]:
            exp_conf[OPERATOR_LIST] = op_list
            rec_stats = get_match_stats_summaries(configuration, match_list,
                                                  exp_conf)
            ope = op_list[-1]
            for att in rec_stats:
                rec[ope+att] = rec_stats[att]
        rec_list.append(rec)
    # Store summarized results
    filename = get_summary_file(configuration, query, '', parameter)
    write_result_file(filename, rec_list, parameter)


def summarize_stats_operators(configuration, match_list, query):
    '''
    Summarize statistical experiments of operators
    '''
    # Result lists
    rec_list = []
    for op_list in configuration[OPERATOR_LIST]:
        exp_conf = get_default_experiment(configuration[PARAMETER])
        exp_conf[QUERY] = query
        exp_conf[OPERATOR_LIST] = op_list
        rec_stats = get_match_stats_summaries(configuration, match_list,
                                              exp_conf)
        rec_stats['operators'] = str(len(op_list))
        rec_list.append(rec_stats)
    # Store summarized results
    filename = get_summary_file(configuration, query, '', 'operators')
    write_result_file(filename, rec_list, 'operators')


def summarize_all(configuration, match_list, run_count):
    '''
    Summarize all results
    '''
    # Get parameter having variation
    for par in get_variated_parameters(configuration):
        for query in configuration[QUERY_LIST]:
            summarize(configuration, match_list, query, par, run_count)


def summarize_all_stats(configuration, match_list):
    '''
    Summarize all statistical results
    '''
    # Get parameter having variation
    for par in get_variated_parameters(configuration):
        for query in configuration[QUERY_LIST]:
            summarize_stats(configuration, match_list, query, par)
        for query in configuration[QUERY_LIST]:
            summarize_stats_operators(configuration, match_list, query)


def confidence_interval(parameter, in_file, out_file):
    '''
    Calculate final result with confidence interval
    '''
    if not os.path.isfile(in_file):
        print 'File does not exists: ' + in_file
        return
    command = CONFINTERVAL_COMMAND.format(inf=in_file, outf=out_file,
                                          keyf=parameter)
    print command
    os.system(command)
    if not os.path.isfile(out_file):
        print 'Output file not found: ' + out_file
        print "Check if 'confinterval' is in path"


def confidence_interval_all(configuration):
    '''
    Calculate confidence interval for all summarized results
    '''
    # For every parameter
    for parameter in get_variated_parameters(configuration):
        for query in configuration[QUERY_LIST]:
            in_file = \
                get_summary_file(configuration, query, SUM_RUN, parameter)
            out_file = \
                get_result_file(configuration, query, SUM_RUN, parameter)
            confidence_interval(parameter, in_file, out_file)
            in_file = \
                get_summary_file(configuration, query, SUM_MEM, parameter)
            out_file = \
                get_result_file(configuration, query, SUM_MEM, parameter)
            confidence_interval(parameter, in_file, out_file)
