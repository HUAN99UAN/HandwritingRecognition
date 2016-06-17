import argparse
import os


class ExpandDirectoryPathAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = self._expand_tilde(values)
        values = self._to_absolute_path(values)
        setattr(namespace, self.dest, values)

    @classmethod
    def _to_absolute_path(cls, path):
        return os.path.abspath(path)

    @classmethod
    def _expand_tilde(cls, path):
        return os.path.expanduser(path)


class ExpandFilePathAction(argparse.Action):
    @classmethod
    def _to_absolute_path(cls, path):
        return os.path.abspath(path)

    @classmethod
    def _expand_tilde(cls, path):
        return os.path.expanduser(path)

    def __call__(self, parser, namespace, values, option_string=None):
        values = ExpandFilePathAction._expand_tilde(values)
        values = ExpandFilePathAction._to_absolute_path(values)
        setattr(namespace, self.dest, values)


class OutputFileAction(ExpandFilePathAction):
    @classmethod
    def create_directory_if_required(cls, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __call__(self, parser, namespace, values, option_string=None):
        path = self._expand_tilde(values)
        path = self._to_absolute_path(path)
        self.create_directory_if_required(path)
        setattr(namespace, self.dest, path)