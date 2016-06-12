import argparse
import sys

from PIL import Image
# Fix path issues
from os.path import dirname, realpath

root = dirname(dirname(realpath(__file__)))
sys.path.append(root)

from inputOutput.openers import ImageOpener
from inputOutput.outputFiles import image_to_file, build_file_path, create_directory
import segmenter.characters.characterSegmenter as characterSegmenter
import utils.actions as actions
import utils.types as types


default_output_extension = "jpg"


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('image', type=str,
                        help='Image of a word to be segmented into characters.')
    parser.add_argument('outputDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory where you want to store the character images.')
    parser.add_argument('--outputExtension', type=str, default=default_output_extension,
                        action=actions.VerifyOutputExtensionAction,
                        help='The extension of the cropped output images. Accepted extension are: {extensions}.'.format(
                            extensions=", ".join(Image.SAVE.keys())))
    parser.add_argument('--white_threshold', type=int,
                        choices=range(0, 256),
                        metavar='',
                        default=characterSegmenter.default_parameters.get('white_threshold'),
                        help='The white_threshold used in segmenting the images, default: {default}. The threshold '
                             'value should be in the in the range (0, 255).'.format(
                            default=characterSegmenter.default_parameters.get('white_threshold')
                        ))
    parser.add_argument('--maximum_word_length', type=types.natural_number_type,
                        default=characterSegmenter.default_parameters.get('maximum_word_length'),
                        help='The maximum length of an input word, default: {default}.'.format(
                            default=characterSegmenter.default_parameters.get('maximum_word_length')
                        ))
    parser.add_argument('--initial_segment_criterion', type=types.natural_number_type,
                        default=characterSegmenter.default_parameters.get('initial_segment_criterion'),
                        help='The initial segment criterion, default: {default}. This value should be a natural number.'.format(
                            default=characterSegmenter.default_parameters.get('initial_segment_criterion')
                        ))
    return vars(parser.parse_args())


def extract_segmenter_parameters(cli_arguments):
    parameters = cli_arguments.copy()
    keys_to_remove = ['image', 'outputDirectory', 'outputExtension']
    for key in keys_to_remove:
        del parameters[key]
    return parameters


def show_segmentation_lines(segmenter, cli_arguments):
    create_directory(cli_arguments.get('outputDirectory'))
    output_file_path = build_file_path(
            path=cli_arguments.get('outputDirectory'),
            file_name='test',
            extension=cli_arguments.get('outputExtension')
    )
    image = segmenter.image.copy()
    for line in segmenter.segmentation_points:
        line.paint_on(image)
    image_to_file(image, output_file_path)


def generate_character_images(segmenter, cli_arguments):
    create_directory(cli_arguments.get('outputDirectory'))
    character_images = segmenter.character_images
    for (number, image) in zip(range(0, len(character_images)), character_images):
        file_path = build_file_path(path=cli_arguments.get('outputDirectory'), file_name='character_{}'.format(number), extension=cli_arguments.get('outputExtension'))
        image_to_file(image, file_path)


def show_baseline_computation(segmenter, cli_arguments):
    output_file_path = build_file_path(
        path=cli_arguments.get('outputDirectory'),
        file_name='baseline_computation',
        extension=cli_arguments.get('outputExtension')
    )
    base_lines = segmenter.base_lines
    image = segmenter.image.copy()
    base_lines.paint(image)
    image_to_file(image, output_file_path)


if __name__ == '__main__':
    Image.init()
    cli_arguments = parse_command_line_arguments()
    parameters = extract_segmenter_parameters(cli_arguments)

    image = ImageOpener(image_file_path=cli_arguments.get('image')).open()
    character_segmenter = characterSegmenter.CharacterSegmenter(word_image=image, parameters=parameters)

    # show_segmentation_lines(character_segmenter, cli_arguments)
    # generate_character_images(character_segmenter, cli_arguments)
    show_baseline_computation(character_segmenter, cli_arguments)
