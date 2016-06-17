import numpy as np
import cv2


class Image(np.ndarray):
    # source: http://docs.scipy.org/doc/numpy-1.10.1/user/basics.subclassing.html

    _show_image_for_ms = 3000

    def __new__(cls, input_array):
        # Create the ndarray instance of our type, given the usual
        # ndarray input arguments.  This will call the standard
        # ndarray constructor, but return an object of our type.
        # It also triggers a call to InfoArray.__array_finalize__
        obj = np.asarray(input_array).view(cls)
        # set the new 'info' attribute to the value passed
        # obj.info = info
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
        if obj is None: return
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
        # self.info = getattr(obj, 'info', None)
        # We do not need to return anything

    def sub_image(self, bounding_box):
        raise NotImplementedError()

    def show(self, window_name = None):
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, self)
        cv2.waitKey(self.__class__._show_image_for_ms)
        cv2.destroyAllWindows()

    @staticmethod
    def from_file(input_file):
        np_image = cv2.imread(input_file)
        image = Image(np_image)
        return image


if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    Image.from_file(image_file)