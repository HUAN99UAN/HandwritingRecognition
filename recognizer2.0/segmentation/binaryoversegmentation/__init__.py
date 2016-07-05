import pickle

from utils.things import Size, Range, NormalDistribution

default_statistics_file_path = './segmentation/binaryoversegmentation/character_image_data.pkl'

with open(default_statistics_file_path) as input_file:
    _character_statistics = pickle.load(input_file)

    # default_minimum_character_size = Size(
    #     width=_character_statistics['min_width'],
    #     height=_character_statistics['min_height'],
    # )

    default_minimum_character_size = Size(
        width=16,
        height=30,
    )

    # default_maximum_character_size = Size(
    #     width=_character_statistics['max_width'],
    #     height=_character_statistics['max_height'],
    # )

    default_maximum_character_size = Size(
        width=70,
        height=100,
    )

    character_width_distribution = NormalDistribution(
        mean=_character_statistics['mean_width'],
        sd=_character_statistics['sd_width'],
    )

    default_num_foreground_pixels = Range(
        _character_statistics['min_pixels'],
        _character_statistics['min_pixels']
    )