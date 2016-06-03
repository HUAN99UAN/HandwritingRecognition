import os
import os.path
import sys


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=False)


def image_to_file(image, file_path):
    try:
        image.save(file_path)
    except KeyError:
        print("Could not write the file {} as the output format could not be determined.".format(
            file_path), file=sys.stderr)
    except IOError:
        print("Could not write the file {} the created file may contain partial data.".format(
            file_path), file=sys.stderr)


def build_file_path(path, file_name, extension):
    file_with_extension = '.'.join([file_name, extension])
    return os.path.join(path, file_with_extension)