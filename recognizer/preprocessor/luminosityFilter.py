import cv2


class LuminosityFilter:

    def __init__(self):
        pass

    def luminosity_normalization(self, img):
        size = img.shape
        y_center = size[0]/2
        x_center = size[1]/2
        center_sqr = img[y_center-500:y_center+500, x_center-500:x_center+500]
        lowest = center_sqr.min()
        highest = center_sqr.max()

        normalized_image = self._linear_norm(img, lowest, highest)
        return normalized_image

    def _linear_norm(self, image, old_min, old_max, new_min = 0, new_max = 255):
        old_range = old_max - old_min
        new_range = new_max - new_min
        normalized_to_old_min_image = image - old_min
        factor = (new_range / old_range)
        return normalized_to_old_min_image * factor + new_min

if __name__ == '__main__':
    img = cv2.imread('test2.jpg', 0)
    l = LuminosityFilter()
    l.luminosity_normalization(img)