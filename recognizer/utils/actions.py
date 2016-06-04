import argparse
import os
from glob import glob

from PIL import Image

Image.init()


class VerifyOutputExtensionAction(argparse.Action):
    @staticmethod
    def _is_valid_output_extension(extension):
        return extension.upper() in Image.SAVE.keys()

    def __call__(self, parser, namespace, values, option_string=None):
        if not VerifyOutputExtensionAction._is_valid_output_extension(values):
            raise ValueError("The extension {} is  not supported.".format(values))
        setattr(namespace, self.dest, values)


class ExpandDirectoryPathAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = ExpandDirectoryPathAction._expand_tilde(values)
        values = ExpandDirectoryPathAction._to_absolute_path(values)
        setattr(namespace, self.dest, values)

    @staticmethod
    def _to_absolute_path(path):
        return os.path.abspath(path)

    @staticmethod
    def _expand_tilde(path):
        return os.path.expanduser(path)


class ExpandFilePathsAction(argparse.Action):
    @staticmethod
    def _to_absolute_path(paths):
        return [os.path.abspath(path) for path in paths]

    @staticmethod
    def _expand_tilde(paths):
        return [os.path.expanduser(path) for path in paths]

    @staticmethod
    def _expand_wild_card(values):
        paths = list()
        if isinstance(values, list):
            [paths.extend(glob(value)) for value in values]
        else:
            paths = list(glob(values))
        return paths

    def __call__(self, parser, namespace, values, option_string=None):
        values = ExpandFilePathsAction._expand_tilde(values)
        values = ExpandFilePathsAction._expand_wild_card(values)
        values = ExpandFilePathsAction._to_absolute_path(values)
        setattr(namespace, self.dest, values)

class PositiveIntegerVerificationAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = ExpandDirectoryPathAction._expand_tilde(values)
        values = ExpandDirectoryPathAction._to_absolute_path(values)
        setattr(namespace, self.dest, values)