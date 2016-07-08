import os

from utils.image import Image
import utils.colors as colors
from inputOutput import wordio
import preprocessing
from utils.shapes import HorizontalLine
from segmentation.binaryoversegmentation.baseline import VerticalHistogram

output_directry = '/Users/laura/Desktop/'

if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/images/jpg/Stanford-CCCC_0072.jpg'
    annotation_file = '/Users/laura/Repositories/HandwritingRecognition/data/labels/Stanford-CCCC_0072.words'

    found_base_line_color = colors.red
    corrected_base_line_color = colors.dark_blue

    image = Image.from_file(image_file)
    preprocessed_image = preprocessing.Pipe().apply(image)

    words_of_interest = [
        {
            'idx': (12, 0),
            'output_file_path':
                '/Users/laura/Repositories/HandwritingRecognition/report/shared/img/method/base_line_fail.png',
            'correct_baselines':
                [lambda image: HorizontalLine(x1=0, x2=image.width, y=24)]
        },
        {
            'idx': (9, 2),
            'output_file_path':
                '/Users/laura/Repositories/HandwritingRecognition/report/shared/img/method/base_line_succes.png'
        }
    ]

    annotation = wordio.read_only_annotation(annotation_file)

    base_line_estimator = VerticalHistogram()

    for woi in words_of_interest:
        line_idx = woi['idx'][0]
        word_idx = woi['idx'][1]
        word = annotation[line_idx][word_idx]

        word_image = preprocessed_image.sub_image(word, remove_white_borders=False)
        low, high = base_line_estimator.estimate(word_image)

        output_image = image.sub_image(word)
        output_image = low.paint_on(output_image, color=found_base_line_color, width=1)
        output_image = high.paint_on(output_image, color=found_base_line_color, width=1)
        for base_line in woi.get('correct_baselines', []):
            output_image = base_line(word_image).paint_on(output_image, color=corrected_base_line_color, width=1)
        output_image.to_file(woi['output_file_path'])