from os import path
import argparse
import pickle

import numpy as np
import progressbar

import utils.actions as actions
from inputOutput import wordio as xmlReader
from utils.image import Image
import segmentation.binaryoversegmentation
import preprocessing


class _StatisticsComputer(object):

    def __init__(self, xml_files, image_directory, preprocessor, image_extension='ppm'):
        self._xml_files = xml_files
        self._image_directory = image_directory
        self._preprocessor = preprocessor
        self._image_extension = image_extension

        self._statistics = {
            'heights': [],
            'widths': [],
            'foreground_pixels': []
        }

    def build(self):
        bar = progressbar.ProgressBar()
        for xml_file in bar(self._xml_files):
            self._add_data_from_file(xml_file)
        self._reject_outliers()
        return self._extract_statistics()

    def _extract_statistics(self):
        self._statistics['mean_height'], self._statistics['sd_height'] = self._mean_and_sd(self._statistics['heights'])
        self._statistics['mean_width'], self._statistics['sd_width'] = self._mean_and_sd(self._statistics['widths'])
        self._statistics['mean_pixels'], self._statistics['sd_pixels'] = self._mean_and_sd(self._statistics['foreground_pixels'])

        self._statistics['min_height'], self._statistics['max_height'] = min(self._statistics['heights']), max(self._statistics['heights'])
        self._statistics['min_width'], self._statistics['max_width'] = min(self._statistics['widths']), max(self._statistics['widths'])
        self._statistics['min_pixels'], self._statistics['max_num_pixels'] = min(self._statistics['foreground_pixels']), max(self._statistics['foreground_pixels'])
        return self._statistics

    def _mean_and_sd(self, data):
        mean = sum(data) / float(len(data))
        sd = np.std(data)
        return mean, sd

    def _reject_outliers(self):
        for key in self._statistics:
            self._statistics[key] = self._reject_outliers_from_list(self._statistics[key])

    def _reject_outliers_from_list(self, list, m=2):
        data = np.array(list)
        return data[abs(data - np.mean(data)) < m * np.std(data)]

    def _add_data_from_file(self, xml_file):
        image, lines = self._get_image_and_lines_from_file(xml_file)
        preprocessed_image = self._preprocessor.apply(image)
        for line in lines:
            self._add_data_from_line(line=line, image=preprocessed_image)

    def _get_image_and_lines_from_file(self, xml_file):
        lines, image_name = xmlReader.read(xml_file)
        image_path = self._build_image_file_path(image_name)
        image = Image.from_file(image_path)
        return image, lines

    def _build_image_file_path(self, image_name):
        return path.join(self._image_directory, image_name + '.' + self._image_extension)

    def _add_data_from_line(self, line, image):
        for word in line:
            self._add_data_from_word(word, image)

    def _add_data_from_word(self, word, image):
        for character in word.characters:
            self._add_data_from_character(character, image)

    def _add_data_from_character(self, character, image):
        if not character.is_valid:
            return
        character_image = image.sub_image(character, remove_white_borders=True)
        if not character_image.is_empty:
            self._statistics['widths'].append(character_image.width)
            self._statistics['heights'].append(character_image.height)
            self._statistics['foreground_pixels'].append(character_image.number_of_foreground_pixels)


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=
                        path.abspath(
                            path.expanduser(
                                segmentation.binaryoversegmentation.default_statistics_file_path
                            )
                        ),
                        action=actions.ExpandFilePathAction,
                        help='The path to the output file.')
    return vars(parser.parse_args())

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    statistics = _StatisticsComputer(
        xml_files=cli_arguments['wordsFiles'],
        image_directory=cli_arguments['imageDirectory'],
        preprocessor=preprocessing.Pipe()
    ).build()

    with open(cli_arguments['outputFile'], 'w') as output_file:
        pickle.dump(statistics, output_file)
