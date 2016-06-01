import numpy as np

from segmenter.words.SuspiciousSegmentationPointGenerator import SuspiciousSegmentationPointGenerator
from errors.inputErrors import InvalidImageError


default_parameters = {
    'white_threshold': 240
}


class WordSegmenter:

    def __init__(self, word_image, parameters={}):
        self._word_image = word_image
        self._parameters = default_parameters.copy()
        self._parameters.update(parameters)
        try:
            validator = WordImageValidator(self._word_image, **self._parameters).validate()
        except:
            raise

    def segment(self):
        ssps = SuspiciousSegmentationPointGenerator(self._word_image, **self._parameters)


class WordImageValidator:

    def __init__(self, image, white_threshold):
        self._image = image
        self._image_array = np.array(image)
        self._white_threshold = white_threshold

    def _is_gray_scale(self):
        if not self._image.mode in ['1', 'L', 'I', 'F']:
            raise InvalidImageError("The word image is not gray scale.")
        else:
            return True

    def _has_foreground(self):
        foreground = self._image_array < self._white_threshold
        if not np.any(foreground):
            raise InvalidImageError('The word image does not have a foreground.')
        else:
            return True

    def validate(self):
        return self._is_gray_scale() and self._has_foreground()
