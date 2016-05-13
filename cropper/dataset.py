from builtins import staticmethod

import annotationTree
import pageImage
import os.path

_image_file_extension = 'jpg'

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
    def from_files(files, image_files_directory):
        data_set = DataSet()
        for words_file in files:
            tree = annotationTree.AnnotationTree(file_path=words_file)
            image_file_name = tree.get_image_file_name()
            image_file_path = _build_file_path(
                path=image_files_directory,
                file_name=image_file_name,
                extension=_image_file_extension
            )
            page_image = pageImage.PageImage(image_file_path, tree)
            data_set.add(page_image, image_file_name)
        return data_set

    def __str__(self):
        return ", ".join([
            "{DataSet",
            "page images: [" + ", ".join(self._pages.keys()) + "]",
            "}"])

def _build_file_name(file_name, extension):
    return '.'.join([file_name, extension])

def _build_file_path(path, file_name, extension=''):
    return os.path.join(path, _build_file_name(file_name, extension))
