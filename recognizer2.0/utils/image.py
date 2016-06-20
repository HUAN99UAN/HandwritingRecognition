import numpy as np
import cv2
from enum import Enum

from utils.things import Range, Size


class ColorMode(Enum):
    gray, bgr, binary = range(3)

    @property
    def is_gray(self):
        return self == ColorMode.gray

    @property
    def is_bgr(self):
        return self == ColorMode.bgr

    @property
    def is_binary(self):
        return self == ColorMode.binary

class InterpolationMethod(Enum):
    nearest_neighbour, bilinear, bicubic = range(3)

    @property
    def as_open_cv(self):
        mapping = {
            self.nearest_neighbour : cv2.INTER_NEAREST,
            self.bilinear : cv2.INTER_LINEAR,
            self.bicubic : cv2.INTER_CUBIC
        }
        return mapping.get(self)

class WrongColorModeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Image(np.ndarray):
    """Representation of an image, images are stored as B G R

    """
    # source: http://docs.scipy.org/doc/numpy-1.10.1/user/basics.subclassing.html

    _default_wait_key = 2000

    def __new__(cls, input_array, color_mode):
        # Create the ndarray instance of our type, given the usual
        # ndarray input arguments.  This will call the standard
        # ndarray constructor, but return an object of our type.
        # It also triggers a call to InfoArray.__array_finalize__
        obj = np.asarray(input_array).view(cls)
        # set the new 'info' attribute to the value passed
        obj._color_mode = color_mode
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(InfoArray, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. InfoArray():
        #    obj is None
        #    (we're in the middle of the InfoArray.__new__
        #    constructor, and self.info will be set when we return to
        #    InfoArray.__new__)
        if obj is None:
            return
        # From view casting - e.g arr.view(InfoArray):
        #    obj is arr
        #    (type(obj) can be InfoArray)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is InfoArray
        #
        # Note that it is here, rather than in the __new__ method,
        # that we set the default value for 'info', because this
        # method sees all creation of default objects - with the
        # InfoArray.__new__ constructor, but also with
        # arr.view(InfoArray).
        self._color_mode = getattr(obj, '_color_mode', ColorMode.bgr)
        # We do not need to return anything

    def sub_image(self, bounding_box):
        """
        Get the sub_image of this image, based on the bounding box. Note that this performs a SHALLOW COPY of the
        original image. Operations performed on the original image DO NOT affect the subimage.
        :param bounding_box: The bounding box like objects, should have the following properties: top, bottom, right,
        left as ints.
        """
        sub_image = self[bounding_box.top:bounding_box.bottom, bounding_box.left:bounding_box.right]
        return Image(sub_image)

    def show(self, wait_key=_default_wait_key, window_name=None):
        """
        Show this image.
        :param wait_key: How long to wait for a key, before closing the image and continuing program execution. Choose
        wait_key=0 if you want the window shown until a key is pressed.
        :param window_name: The name of the window.
        """
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, self)
        cv2.waitKey(wait_key)
        cv2.destroyAllWindows()

    def resize(self, width=None, height=None, keepaspect_ratio=True, interpolation_method=InterpolationMethod.bilinear):
        """
        Resize an image to a new size. Note that the aspect ratio of the image is not take into account.
        :param width: The width of the new image, if only width is given keep_aspect_ratio is set to True.
        :param height: The height of the new image, if only height is given keep_aspect_ratio is set to True.
        :param keepaspect_ratio: if the apsect ratio is to be kept intact, is True, unless both width and height are passed.
        :param interpolation_method: The interpolation method to use, default is bilinear. Should be either an
        image.InterpolateMethod or cv2.INTER_*
        :return: A new image of size new_size.
        """
        def compute_ratio(base_value, other_value):
            return base_value / float(other_value)

        def compute_new_size(image, width, height, keep_aspect_ratio):
            if width and not height:
                ratio = compute_ratio(width, image.width)
                height = round(ratio * image.height)
                return Size(width=int(width), height=int(height))
            if height and not width:
                ratio = compute_ratio(height, image.height)
                width = round(ratio * image.width)
                return Size(width=int(width), height=int(height))
            if height and width and keep_aspect_ratio:
                ratio = min(compute_ratio(height, image.height), compute_ratio(width, image.width))
                width = ratio * image.width
                height = ratio*image.height
                return Size(width=int(width), height=int(height))
            if height and width and not keep_aspect_ratio:
                return Size(width=int(width), height=int(height))
            raise TypeError('Invalid combination of arguments.')

        def verify_size(size):
            if size.width < 1 or size.height < 1:
                raise KeyError('Both width and height should be >= 1.')

        correct_size = compute_new_size(self, width, height, keepaspect_ratio)
        verify_size(correct_size)

        scaled_image = cv2.resize(src=self, dsize=correct_size, interpolation=interpolation_method.as_open_cv)
        return Image(scaled_image, self.color_mode)

    @property
    def width(self):
        shape = self.shape
        return shape[1]

    @property
    def height(self):
        shape = self.shape
        return shape[0]

    @property
    def dimension(self):
        shape = self.shape
        return Size(width=shape[1], height=shape[0])

    @property
    def luminosity_range(self):
        if self.color_mode in [ColorMode.gray, ColorMode.binary]:
            return Range(
                min=np.min(self), max=np.max(self)
            )
        else:
            raise NotImplementedError("Luminosity range is not supported for color images.")

    @property
    def color_mode(self):
        return self._color_mode

    @staticmethod
    def from_file(input_file):
        np_array = cv2.imread(input_file, cv2.IMREAD_COLOR)
        image = Image(np_array, color_mode=ColorMode.bgr)
        return image


if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    image = Image.from_file(image_file)
    import preprocessing.colorspaces
    gray_scale = preprocessing.colorspaces.ToGrayScale().apply(image)
    image.show()
