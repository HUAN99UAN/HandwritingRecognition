import inputOutput.wordio
import argparse
import inputOutput.actions
from preprocessing import pipe
from featureExtraction import crossings
from os import path
from utils import image

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('words_file', metavar='wordsFile', type=str,
                        action=inputOutput.actions.ExpandFilePathAction,
                        help='The words file')

    parser.add_argument('image', metavar='image', type=str,
                        action=inputOutput.actions.ExpandFilePathAction,
                        help='The image with the text that is to be read.')

    parser.add_argument('outputFilePath', metavar='outputWordsFile', type=str,
                        action=inputOutput.actions.ExpandFilePathAction,
                        help='The path output file.')
    return vars(parser.parse_args())


class _ModelBuilder(object):

    def __init__(self, feature_extractor, word_files, image_directory):
        """

        :param feature_extractor:
        :param word_files:
        :param image_directory:
        """
        self._feature_extractor = feature_extractor
        self._word_files = word_files
        self._image_directory = image_directory
        self._model = {}

    def build(self, xmlfile):
        """

        :return:
        """
        # TODO read words file, gives words, characters, and image_name
        words, characters, image_name = inputOutput.wordio.read(xmlfile)

        # TODO create the path with the name of the file PYTHON STUFF
        image_path = path.join(self._image_directory, image_name + '.jpg')

        # TODO read image
        img = image.Image.from_file(image_path)

        # TODO do pre-processing
        p = pipe.Pipe()
        pre_processed_img = p.apply(img)

        for character in characters:

            # TODO crop stuff
            cropped_character = pre_processed_img.sub_image(character)
            # TODO extract features
            feature = self._feature_extractor.extract(cropped_character)
            self.check_if_ch_exists(character.text)
        # TODO store in the model



        # {'a': [feature_1, feature2]}

    def check_if_ch_exists(self, ch, feature):
        if ch in self._model:
            self.update_ch(ch, feature)
        else:
            self.add_ch(ch, feature)

    def add_ch(self, ch, feature):
        self._model[ch] = [feature]

    def update_ch(self, ch, feature):
        self._model[ch] += feature




if __name__ == '__main__':
    #arguments = parse_command_line_arguments()

    m = _ModelBuilder(crossings.Crossings(), ['Stanford-CCCC_0092.words'], '/home/angelo/Documents/HandwritingRecognition/data/pages/Stanford')
    m.build('Stanford-CCCC_0092.words')
    # for xml in ['test.words']:
    #     tmp = wordio.read(xml)
    #     break

    # print tmp
