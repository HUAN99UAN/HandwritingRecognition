import string
import pickle
import math

import numpy as np
from scipy.spatial import distance

from classification import GeneralModel
from utils.image import Image, ColorMode


required_image_width_in_pixels = 252


def compute_feature_set_differences(a, b):
    distance_matrix = distance.cdist(a, b)
    unique_distances = np.triu(distance_matrix, 1)
    distance_sum = np.sum(unique_distances, axis=(0,1))
    number_of_unique_elements = (distance_matrix.shape[0] * distance_matrix.shape[1]) / 2 + max(distance_matrix.shape[0], distance_matrix.shape[1])
    mean_distance = distance_sum / number_of_unique_elements
    return mean_distance


def compute_difference_matrix(model):
    relevant_keys = sorted(
        [
            key
            for key
            in model.keys()
            if (
                key in string.ascii_lowercase and
                not key == ''
            )
            ]
    )
    difference_matrix = np.empty((len(relevant_keys), len(relevant_keys)))

    for a_idx, a_key in enumerate(relevant_keys):
        for b_idx, b_key in enumerate(relevant_keys):
            if b_idx <= a_idx:
                mean_distance = compute_feature_set_differences(model.get(a_key), model.get(b_key))
                difference_matrix[a_idx, b_idx] = difference_matrix[b_idx, a_idx] = mean_distance
    return difference_matrix


def visualize_distance_matrix(distance_matrix):
    maximum_value = np.max(distance_matrix)
    minimum_value = np.min(distance_matrix)

    color_matrix = (1 - ((distance_matrix - minimum_value) / (maximum_value - minimum_value))) * 255
    matrix_image = Image(color_matrix, ColorMode.gray)
    width_scale = math.floor(required_image_width_in_pixels / matrix_image.width)
    matrix_image = matrix_image.resize(width=width_scale * matrix_image.width)
    return matrix_image

if __name__ == '__main__':
    model_file = '/Users/laura/Repositories/HandwritingRecognition/recognizer2.0/model.pkl'
    distance_matrix_file = '/Users/laura/Desktop/distance_matrix.pkl'
    image_output_file = '/Users/laura/Repositories/HandwritingRecognition/report/individual/img/discussion/distance.png'

    # model = GeneralModel.read_from_file(model_file)
    # distance_matrix = compute_difference_matrix(model)

    # with open(distance_matrix_file, 'wb+') as output_file:
    #     pickle.dump(distance_matrix, output_file)

    with open(distance_matrix_file) as input_file:
        distance_matrix = pickle.load(input_file)
    
    image = visualize_distance_matrix(distance_matrix)
    image.show(window_name='Final result', wait_key=0)
    image.to_file(image_output_file)

