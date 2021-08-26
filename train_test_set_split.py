import glob
import os
import random
import shutil


def split(path='datasets/piano'):
    file_list = glob.glob(path + '/' + '*.npy')
    random.shuffle(file_list)
    list_size = len(file_list)
    separate_index = int(0.9 * list_size)
    if not os.path.exists(path):
        os.mkdir(path)
    train_dir = path + '/' + 'train'
    test_dir = path + '/' + 'test'
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    for f in file_list[:separate_index]:
        shutil.copy(f, train_dir)
    for f in file_list[separate_index:]:
        shutil.copy(f, test_dir)


def remove_original(path='datasets/piano'):
    file_list = glob.glob(path + '/' + '*.npy')
    for f in file_list:
        os.remove(f)
