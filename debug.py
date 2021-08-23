import glob
import os


def file_number(path, extension='*'):
    return len(glob.glob(path + '/' + '*.' + extension))


def file_keep_extension(path, extension=None):
    if extension is None:
        extension = []

    for item in os.listdir(path):
        to_remove = True
        for e in extension:
            if item.endswith(e):
                to_remove = False
                break

        if to_remove:
            print('Removing:', item)
            os.remove(os.path.join(path, item))


def test():
    print(file_number('arcade'))
    # file_keep_extension(path='arcade', extension=['mid', 'midi'])
