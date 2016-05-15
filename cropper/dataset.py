from builtins import staticmethod

import annotationTree
import inputElements
import pageImage
import os.path


class DataSet:

    def __init__(self):
        self._pages = dict()

    def add(self, page_image, description=None):
        if not description:
            description = page_image.image_file
        self._pages.update({
            description: page_image
        })

    @staticmethod
    def from_files(words_files, image_files_directory):
        return DataSetBuilder(words_files, image_files_directory).build()

    def __str__(self):
        return ", ".join([
            "{DataSet",
            "page images: [" + ", ".join(self._pages.keys()) + "]",
            "}"])


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
            image_file_name = tree.get_image_file_name()
            image_file_path = self._build_image_file_path(image_file_name,)
            image = pageImage.ImageOpener(image_file_path).open()
            page_image = inputElements.PageImage(
                description=image_file_name,
                image=image,
                tree=tree
            )
            print(page_image)
            data_set.add(page_image, image_file_name)
        return data_set