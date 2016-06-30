import pickle

from utils.things import Size, NormalDistribution

default_statistics_file_path = './segmentation/binaryoversegmentation/character_image_data.pkl'

with open(default_statistics_file_path) as input_file:
    character_statistics = pickle.load(input_file)

    default_minimum_character_size = Size(
        width=character_statistics['min_width'],
        height=character_statistics['min_height'],
    )

    default_maximum_character_size = Size(
        width=character_statistics['max_width'],
        height=character_statistics['max_height'],
    )

    character_height_distribution = NormalDistribution(
        mean=character_statistics['mean_height'],
        sd=character_statistics['sd_height'],
    )

    character_width_distribution = NormalDistribution(
        mean=character_statistics['mean_width'],
        sd=character_statistics['sd_width'],
    )