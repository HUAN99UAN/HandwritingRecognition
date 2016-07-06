import os
import pickle

from sklearn.cross_validation import KFold
from progressbar import ProgressBar

from inputOutput import cli_interface, wordio
import preprocessing, segmentation, featureExtraction, classification, postprocessing, recognizer, statistics
from utils.image import Image


pre_processor = preprocessing.Pipe()
segmentor = segmentation.BinaryOverSegmentation()
feature_extractor = featureExtraction.Crossings()
classifier = classification.KNN
model_builder = classification.KNN
post_processor = postprocessing.NearestLexiconEntryWithPrior(
    distance_measure=postprocessing.distances.edit_distance
)


image_directory = None
output_directory = "/Users/laura/Repositories/HandwritingRecognition/data/results/binarysegmentation"


def k_fold_cross_validation(word_files, k=10):
    bar = ProgressBar(max_value=k)
    results = list()
    for train_files, test_files in bar(folds(word_files, k)):
        fold_result = run_fold(train_files, test_files)
        results.append(fold_result)
    return results


def folds(word_files, n_folds):
    number_of_word_files = len(word_files)
    the_folds = KFold(number_of_word_files, n_folds=min(n_folds, number_of_word_files), shuffle=True)
    for train_idx, test_idx in the_folds:
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
    r = recognizer.Recognizer(
        preprocessor=pre_processor,
        segmenter=segmentor,
        feature_extractor=feature_extractor,
        classifier=the_classifier,
        postprocessor=post_processor
    )

    errors = []
    for test_file in test_files:
        error = classify_file(r, test_file)
        if error:
            errors.append(error)

    return {
        'train_data': train_files,
        'test_data': test_files,
        'errors': errors
    }


def build_file_path(directory, base_name, extension):
    return "".join([os.path.join(directory, base_name), extension])


def build_intermediate_output_file_path(annotation_file_path):
    _, base_name = os.path.split(annotation_file_path)
    return build_file_path(output_directory, base_name, '')


def build_image_path(base_name):
    return build_file_path(image_directory, base_name, '.ppm')


def classify_file(the_recognizer, words_file):
    annotation, image_name = wordio.read(words_file)
    image = Image.from_file(build_image_path(image_name))
    read_text = the_recognizer.recognize(
        annotation=annotation,
        image=image
    )
    output_file = build_intermediate_output_file_path(words_file)
    wordio.save(read_text, output_file)
    try:
        return statistics.ClassificationErrorComputer(
            oracle=annotation,
            result=read_text
        ).error
    except ZeroDivisionError:
        return None
    except TypeError:
        return None


def write_results(result, path):
    with open(path, 'w') as output_file:
        pickle.dump(result, output_file)


if __name__ == '__main__':
    (image_directory, word_files, final_results_file_path) = cli_interface.parse_imagedir_wordsfiles_optionaloutputFile(
        default_output_file='/Users/laura/Repositories/HandwritingRecognition/data/results/binarysegmentation/final.pkl'
    )
    results = k_fold_cross_validation(word_files, 2)
    write_results(results, final_results_file_path)
