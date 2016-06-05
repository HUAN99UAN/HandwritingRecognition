import os.path
import warnings
import random
import string

import cropper.annotationTree as annotationTree
import cropper.inputElements as inputElements
import model
import errors
from inputOutput.openers import ImageOpener


def _id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class DataSet:

    def __init__(self):
        self._pages = dict()

    def add(self, page_image, description=None):
        if not description:
            description = _id_generator()
        self._pages.update({
            description: page_image
        })

    def pages(self):
        for key, page in self._pages.items():
            yield (key, page)

    def _page_element_iterator(self, getter):
        for _, page in self.pages():
            for key, element in getter(page):
                yield (key, element)

    def lines(self):
        return self._page_element_iterator(inputElements.PageImage.lines)

    def words(self):
        return self._page_element_iterator(inputElements.PageImage.words)

    def characters(self):
        return self._page_element_iterator(inputElements.PageImage.characters)

    def to_cropped_images_hierarchy(self, directory, extension):
        for _, page in self.pages():
            page.images_to_file(directory=directory, extension=extension, element_getter=extension)

    def pre_process(self, pre_processor):
        for _, page in self.pages():
            page.preprocessed_np_array = pre_processor(page.image_as_np_array)

    def extract_features(self, feature_extractor):
        for _, character in self.characters():
            character.feature_vector = feature_extractor(character.preprocessed_np_array)

    def to_model(self):
        data_set_model = model.Model()
        for _, page in self.pages():
            page_model = page.to_model()
            data_set_model.merge_with(page_model)
        return data_set_model

    def update_annotation_trees(self):
        for _, page in self.pages():
            page.tree.update_from_page_image(page)

    @staticmethod
    def from_files(words_files, image_files_directory):
        return DataSetBuilder(words_files, image_files_directory).build()

    @staticmethod
    def test_data(words_file, image_file):
        return _TestDataSetBuilder(
            words_file = words_file,
            image_file = image_file).build()

    def __str__(self):
        return ", ".join([
            "{DataSet",
            "page images: [" + ", ".join(self._pages.keys()) + "]",
            "}"])


class _TestDataSetBuilder:

    def __init__(self, words_file, image_file):
        self._words_file = words_file
        self._image_file = image_file

    @property
    def image_file_name(self):
        return os.path.basename(self._image_file)

    def build(self):
        data_set = DataSet()
        tree = annotationTree.AnnotationTree(file_path=self._words_file)
        # Allow the Image Opener to crash the program if it encounters problems.
        image = ImageOpener(self._image_file).open()
        page_image = inputElements.PageImage(
            description=self.image_file_name,
            image=image,
            tree=tree
        )
        data_set.add(page_image=page_image, description=self.image_file_name)
        return data_set


class DataSetBuilder:

    def __init__(self, words_files, image_files_directory, image_file_extension = 'jpg'):
        self._words_files = words_files
        self._image_files_directory = image_files_directory
        self._image_file_extension = image_file_extension

    def _build_image_file_name(self, file_name):
        return '.'.join([file_name, self._image_file_extension])

    def _build_image_file_path(self, file_name):
        return os.path.join(self._image_files_directory, self._build_image_file_name(file_name))

    def build(self):
        data_set = DataSet()
        for words_file in self._words_files:
            tree = annotationTree.AnnotationTree(file_path=words_file)
            image_file_name = tree.image_file_name
            image_file_path = self._build_image_file_path(image_file_name)
            try:
                image = ImageOpener(image_file_path).open()
                page_image = inputElements.PageImage(
                    description=image_file_name,
                    image=image,
                    tree=tree
                )
                data_set.add(page_image, image_file_name)
            except errors.fileErrors.NonExistentFileError:
                warnings.warn(
                    'Skipping the file {words_file} as the image {image_file} it annotates cannot be found.'
                        .format(words_file=words_file, image_file=image_file_path)
                )
            except IOError:
                warnings.warn(
                    'Skipping the file {words_file} as the image {image_file} could not be read.'
                        .format(words_file=words_file, image_file=image_file_path)
                )
            except:
                raise
        return data_set