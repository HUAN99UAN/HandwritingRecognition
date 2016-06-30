import pickle

from utils.things import Size

with open('./segmentation/binaryoversegmentation/character_image_data.pkl') as input_file:
    character_statistics = pickle.load(input_file)

    default_minimum_character_size = Size(
        width=character_statistics['minimum_width'],
        height=character_statistics['minimum_height'],
    )

    default_maximum_character_size = Size(
        width=character_statistics['maximum_width'],
        height=character_statistics['maximum_height'],
    )