import argparse
import os
from glob import glob

from PIL import Image


class VerifyOutputExtensionAction(argparse.Action):
    @staticmethod
    def _is_valid_output_extension(extension):
        return extension.upper() in Image.SAVE.keys()

    def __call__(self, parser, namespace, values, option_string=None):
        if not VerifyOutputExtensionAction._is_valid_output_extension(values):
            raise ValueError("The extension {} is  not supported.".format(values))
        setattr(namespace, self.dest, values)


class ExpandWordFilesPathsAction(argparse.Action):
    @staticmethod
    def _expand_wild_card(values):
        paths = list()
        if isinstance(values, list):
            [paths.extend(glob(value)) for value in values]
        else:
            paths = list(glob(values))
        return paths

    @staticmethod
    def _to_absolute_path(paths):
        return [os.path.abspath(path) for path in paths]

    def __call__(self, parser, namespace, values, option_string=None):
        values = ExpandWordFilesPathsAction._expand_wild_card(values)
        values = ExpandWordFilesPathsAction._to_absolute_path(values)
        setattr(namespace, self.dest, values)