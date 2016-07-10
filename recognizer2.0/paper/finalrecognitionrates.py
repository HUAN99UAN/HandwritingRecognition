import argparse
import pickle
import collections
from math import log10, floor

import numpy as np

import utils.actions as actions


Statistics = collections.namedtuple('Statistics', ['mean', 'sd', 'min', 'max'])


def compute_errors(result_files):
    errors = list()
    for result_file in result_files:
        result = read_result_file(result_file)
        errors.append(
            compute_error(result)
        )


def read_result_file(result_file):
    with open(result_file) as input_file:
        return pickle.load(input_file)


def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(x))) - 1)

def stats_to_latex_friendly_string(stats):
    return ' & '.join([str(round_sig(stat)) for stat in stats])


def latex_friendly_print_results(binary_stats, validation_stats):
    binary_string = stats_to_latex_friendly_string(binary_stats)
    validation_string = stats_to_latex_friendly_string(validation_stats)
    final_string = '{validation} & {binary} \\\\'.format(
        validation=validation_string,
        binary=binary_string
    )
    print(final_string)


def compute_error(result):
    binary_results = list()
    validation_results = list()
    for fold in result:
        binary_results.extend(fold.get('binary'))
        validation_results.extend(fold.get('validation'))

    binary_stats = compute_statistics(binary_results)
    validation_stats = compute_statistics(validation_results)
    latex_friendly_print_results(binary_stats, validation_stats)


def compute_statistics(errors):
    return Statistics(
        mean=np.mean(errors),
        sd=np.std(errors),
        min=np.min(errors),
        max=np.max(errors)
    )


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Read the final.pkl file(s) generated by LOOCV script and compute the final error(s).'
    )
    parser.add_argument('result_files', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The file with the results from the LOOCV script.')
    return parser.parse_args().result_files


if __name__ == '__main__':
    files = parse_command_line_arguments()
    compute_errors(result_files=files)