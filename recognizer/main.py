import argparse
import os
import fnmatch

from cropper.dataset import DataSet
from preprocessor import pipe

def recursive_search(directory, ext='words'):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.'+ext):
            matches.append(os.path.join(root, filename))
    return matches

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('word_test_dir', metavar='wrdTest', type=str,
                        help='directory for the test images (words)')

    parser.add_argument('word_training_dir', metavar='wrdTrain', type=str,
                        help='directory for the trainning images (words)')

    parser.add_argument('xml_test_dir', metavar='xmlTest', type=str,
                        help='directory for the labeled xml (words)')

    parser.add_argument('xml_training_dir', metavar='xmlTrain', type=str,
                        help='directory for the labeled xml (characters)')

    return vars(parser.parse_args())


def remove_noise_from(dataset):
    for _, page in dataset.pages():
        page.preprocessed_np_array = pipe.pipe(page.image_as_np_array)


if __name__ == '__main__':
    arguments = parse_command_line_arguments()

    xml_test_files = recursive_search(arguments['xml_test_dir'])
    xml_trainning_files = recursive_search(arguments['xml_training_dir'])

    train_data = DataSet.from_files(
        words_files=xml_trainning_files,
        image_files_directory=arguments['word_training_dir']
    )

    test_data = DataSet.from_files(
        words_files=xml_test_files,
        image_files_directory=arguments['word_test_dir']
    )

    remove_noise_from(train_data)
    remove_noise_from(test_data)

    # remove noise from train and test data

    # segment test_data

    # train classifier

    # classify test data









