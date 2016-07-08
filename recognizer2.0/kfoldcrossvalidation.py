import os
import pickle
import argparse

from sklearn.cross_validation import KFold
from progressbar import ProgressBar


import utils.actions as actions
from inputOutput import  wordio
import preprocessing, segmentation, featureExtraction, classification, postprocessing, recognizer, statistics
from utils.image import Image


pre_processor = preprocessing.Pipe()
feature_extractor = featureExtraction.Crossings()
classifier = classification.KNN
model_builder = classification.KNN
post_processor = postprocessing.NearestLexiconEntryWithPrior(
    distance_measure=postprocessing.distances.edit_distance
)


keys = ['binary', 'validation']
error_computers = {
    'validation': lambda oracle, actual: statistics.ClassificationErrorComputer(
        oracle=oracle, result=actual, skip_non_segmented=True
    ),
    'binary': lambda oracle, actual: statistics.ClassificationErrorComputer(
        oracle=oracle, result=actual, skip_non_segmented=False
    )
}

intermediate_output_directories = {
    'validation': "validationsegmentation",
    'binary': "binarysegmentation",
}

segmenters = {
    'validation': lambda annotation: segmentation.ValidationSegmentation(annotation_file=annotation),
    'binary': lambda annotation: segmentation.BinaryOverSegmentation()
}

image_directory = None
output_directory = None


def k_fold_cross_validation(word_files, k=10, folds_to_skip=0):
    bar = ProgressBar(max_value=k)
    results = list()
    for train_files, test_files in bar(folds(word_files, k, folds_to_skip)):
        fold_result = run_fold(train_files, test_files)
        results.append(fold_result)
    return results


def folds(word_files, n_folds, folds_to_skip):
    number_of_word_files = len(word_files)
    the_folds = KFold(number_of_word_files, n_folds=min(n_folds, number_of_word_files))
    for train_idx, test_idx in list(the_folds)[folds_to_skip:]:
        train_files = [word_files[idx] for idx in train_idx]
        test_files = [word_files[idx] for idx in test_idx]
        yield train_files, test_files


def run_fold(train_files, test_files):
    model = model_builder.build_model(
        xml_files=train_files,
        image_directory=image_directory,
        preprocessor=pre_processor,
        feature_extractor=feature_extractor
    )
    the_classifier = classifier(model=model)

    result = {
        'train_data': train_files,
        'test_data': test_files,
    }

    for key in keys:
        errors = []
        for test_file in test_files:
            r = recognizer.Recognizer(
                preprocessor=pre_processor,
                segmenter=segmenters.get(key)(test_file),
                feature_extractor=feature_extractor,
                classifier=the_classifier,
                postprocessor=post_processor
            )
            error = classify_file(r, test_file, key)
            if error:
                errors.append(error)
        result[key] = errors
    return result


def build_file_path(directory, base_name, extension):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return "".join([os.path.join(directory, base_name), extension])


def build_intermediate_output_file_path(key, annotation_file_path):
    _, base_name = os.path.split(annotation_file_path)
    directory = os.path.join(output_directory, intermediate_output_directories[key])
    return build_file_path(directory, base_name, '')


def build_image_path(base_name):
    return build_file_path(image_directory, base_name, '.ppm')


def classify_file(the_recognizer, words_file, key):
    annotation, image_name = wordio.read(words_file)
    image = Image.from_file(build_image_path(image_name))
    read_text = the_recognizer.recognize(
        annotation=annotation,
        image=image
    )
    output_file = build_intermediate_output_file_path(key, words_file)
    wordio.save(read_text, output_file)
    try:
        return error_computers.get(key)(annotation, read_text).error
    except ZeroDivisionError:
        return None
    except TypeError:
        return None


def write_results(result, output_directory):
    path = build_file_path(output_directory, 'final', extension='.pkl')
    with open(path, 'w') as output_file:
        pickle.dump(result, output_file)


def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('outputDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the output file.')
    parser.add_argument('--skipFolds', type=str,
                        default=0,
                        help='The number of folds to skip.')
    arguments = vars(parser.parse_args())
    return arguments['imageDirectory'], arguments['wordsFiles'], arguments['outputDirectory'], int(arguments['skipFolds'])


if __name__ == '__main__':
    (image_directory, word_files, output_directory, folds_to_skip) = parse_cli()
    results = k_fold_cross_validation(word_files, len(word_files), folds_to_skip)
    write_results(results, output_directory)
