from inputOutput import ImageOpener
from lines import lineSegmenter

if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmenter/final.jpg'
    image = ImageOpener(image_file_path=image_path).open()
    l = lineSegmenter.LineSegmenter(image=image)
    l.segment()

    image = l.paint_stripes()
    image = l.paint_piece_wise_separating_lines(image)
    image.show()
