import preprocessing, segmentation
import inputOutput.wordio as inputOutput
from utils.image import Image
from utils.shapes import Rectangle
from utils import colors

word_box_color = colors.red
character_box_color = colors.dark_blue


def draw(image_to_draw_on, segmentation_image, annotation):
    for line in annotation:
        for word in line:
            image = Rectangle(
                corner=(word.left, word.top),
                opposite_corner=(word.right, word.bottom)
            ).paint_on(image, color=character_box_color, filled=False)

def draw_character_boxes(image_to_draw_on, segmentation_image, word_bounding_box):
    word_image = segmentation_image.sub_image(word_bounding_box)
    character_images =

if __name__ == '__main__':
    annotation_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.words'
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'

    annotation, _ = inputOutput.read(annotation_file)

    preprocessor = preprocessing.Pipe
    segmenter = segmentation.ValidationSegmentation(annotation)

    image = Image.from_file(image_file)
    preprocessed_image = preprocessor.apply(image)

