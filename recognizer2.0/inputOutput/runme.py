import wordio
import argparse
import actions
import cv2
from utils import image
from preprocessing import luminosity, morphological, otsu

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('words_file', metavar='wordsFile', type=str,
                        action=actions.ExpandFilePathAction,
                        help='The words file')

    parser.add_argument('image', metavar='image', type=str,
                        action=actions.ExpandFilePathAction,
                        help='The image with the text that is to be read.')

    parser.add_argument('outputFilePath', metavar='outputWordsFile', type=str,
                        action=actions.ExpandFilePathAction,
                        help='The path output file.')
    return vars(parser.parse_args())


class _ModelBuilder(object):

    def __init__(self, pre_processing_filter, feature_extractor, word_files, image_directory):
        """

        :param pre_processing_filter:
        :param feature_extractor:
        :param word_files:
        :param image_directory:
        """
        self._pre_processing_filter = pre_processing_filter
        self._feature_extractor = feature_extractor
        self._word_files = word_files
        self._image_directory = image_directory

    def build(self, xmlfile):
        """

        :return:
        """
        # TODO read words file, gives words, characters, and image_name
        words, characters, image_name = wordio.read(xmlfile)

        # TODO create the path with the name of the file
        image_path = self._image_directory+'/'+image_name

        # TODO read image
        img = cv2.imread(image_path)

        # TODO do pre-processing
        img_after_luminosity = luminosity.HistogramsEqualization.apply(img)
        img_after_binary = otsu.OtsuMethod.apply(img_after_luminosity)
        img_after_morpho = morphological.Opening.apply(img_after_binary)
        for character in characters:
            pass
            # TODO crop stuff
            cropped_character = image.Image.sub_image(character)
            # TODO extract features
            features = self._feature_extractor(cropped_character)
        # TODO store in the model



if __name__ == '__main__':
    arguments = parse_command_line_arguments()

    for xml in ['Stanford-test-40.words', 'Stanford-test-42.words',
                'Stanford-test-44.words', 'Stanford-test-45.words',
                'Stanford-test-46.words']:
        tmp = wordio.read(xml)
        break

    print tmp
