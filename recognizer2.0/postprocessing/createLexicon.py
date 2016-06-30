from externalLexiconText import ExternalLexiconText
from externalLexiconXML import ExternalLexiconXML
import argparse
import os


class CreateExternalLexicon():
    def __init__(self):
        pass

    @staticmethod
    def _get_files(directory, extension):
        files = []
        for f in os.listdir(directory):
            if f.endswith(extension):
                files.append(f)
        return files


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('xml', metavar='xml_files', type=str,
                        help='The directory for the XML files.')
    parser.add_argument('txt', metavar='txt_files', type=str,
                        help='The directory for text files.')

    return vars(parser.parse_args())


if __name__ == '__main__':
    # cli_arguments = parse_command_line_arguments()
    # print cli_arguments

    XML = ExternalLexiconXML('form="')
    TXT = ExternalLexiconText()
    #
    XML.execute(['1999.02.0055.xml', '1999.02.0010.xml'])
    TXT.execute(['lexicon1.txt', 'lexicon2.txt'])

    TXT._save('mofow.pkl', 'mofoc.pkl')

    data = TXT._load('mofow.pkl', 'mofoc.pkl')

    print '===================='
    print data['word_model']
    print '===================='
    print data['ch_model']
    print '===================='
