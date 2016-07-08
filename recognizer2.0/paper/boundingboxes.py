from utils.image import Image
from utils.shapes import Rectangle
from utils.things import Point, BoundingBox
from utils import colors
from inputOutput import wordio


class BoundingBoxPainter:

    def __init__(self, image_file=None, image=None, annotation=None, annotation_file=None,
                 internal_parameters={}, external_parameters={}):
        self._interal_parameters = internal_parameters
        self._external_parameters = external_parameters

    def paint(self, image_file=None, image=None, annotation=None, annotation_file=None):
        image = Image.from_file(image_file) if image is None else image
        annotation = wordio.read_only_annotation(annotation_file) if annotation is None else annotation

        for line in annotation:
            image = self._paint_line_bounding_boxes(image, line)
        return image

    def _paint_line_bounding_boxes(self, image, line):
        for word in line:
            image = self._paint_word_bounding_boxes(image, word)
        return image

    def _paint_word_bounding_boxes(self, image, word):
        image = self._paint_external_bounding_box(image, word)
        image = self._paint_internal_bounding_boxes(image, word)
        return image

    def _paint_external_bounding_box(self, image, word):
        bounding_box = Rectangle(
            corner=Point(x=word.left, y=word.top),
            opposite_corner=Point(x=word.right, y=word.bottom)
        )
        return bounding_box.paint_on(image, **self._external_parameters)

    def _paint_internal_bounding_boxes(self, image, word):
        for character in word.characters:
            image = self._paint_internal_bounding_box(image, character)
        return image

    def _paint_internal_bounding_box(self, image, character):
        bounding_box = Rectangle(
            corner=Point(x=character.left, y=character.top),
            opposite_corner=Point(x=character.right, y=character.bottom)
        )
        return bounding_box.paint_on(image, **self._interal_parameters)


if __name__ == '__main__':
    image_files = [
        '/Users/laura/Repositories/HandwritingRecognition/data/images/jpg/KNMP-VIII_F_69______2C2O_0004.jpg',
        '/Users/laura/Repositories/HandwritingRecognition/data/images/jpg/Stanford-CCCC_0072.jpg'
    ]
    annotation_files = [
        '/Users/laura/Repositories/HandwritingRecognition/data/labels/KNMP-VIII_F_69______2C2O_0004.words',
        '/Users/laura/Repositories/HandwritingRecognition/data/labels/Stanford-CCCC_0072.words'
    ]

    output_files = [
        '/Users/laura/Dropbox/Studie/Handwriting Recognition/individual/img/introduction/bohemians.png',
        '/Users/laura/Dropbox/Studie/Handwriting Recognition/individual/img/introduction/oldEnglishHomilies.png'
    ]

    bounding_boxes = [
        lambda image: BoundingBox(left=0, right=image.width-1, top=1100, bottom=1950),
        lambda image: BoundingBox(left=0, right=image.width - 1, top=1250, bottom=2100)
    ]

    internal_settings = {
        'color': colors.red,
        'width': 2,
        'filled': False
    }

    external_settings = {
        'color': colors.dark_blue,
        'width': 8,
        'filled': False
    }

    painter = BoundingBoxPainter(
        external_parameters=external_settings,
        internal_parameters=internal_settings
    )

    for idx, image_file in enumerate(image_files):
        image = painter.paint(image_file=image_file, annotation_file=annotation_files[idx])
        section = image.sub_image(
            bounding_box=bounding_boxes[idx](image),
            remove_white_borders=False
        )
        section.to_file(output_file=output_files[idx])
