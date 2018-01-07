import argparse
from os import getcwd
from os.path import basename, exists, join, splitext
from math import isclose
from collections import namedtuple
from PIL import Image


def create_parser():
    parser = argparse.ArgumentParser(prog='Image Resizer')
    parser.add_argument('filepath', help='Path to original image', type=str)
    parser.add_argument('--scale', help='Float, positive', type=float)
    parser.add_argument('--width', help='Integer, positive', type=int)
    parser.add_argument('--height', help='Integer, positive', type=int)
    parser.add_argument('--newpath', help='Where to save new image', type=str)
    parser.add_argument('--newname', help='New name without ext.', type=str)
    return parser


def open_image(path):
    return Image.open(path)


def get_old_img_params(img_object, path):
    old_img_params = {}
    old_img_params['name'] = splitext(basename(path))[0]
    old_img_params['ext'] = splitext(basename(path))[1]
    old_img_params['size'] = img_object.size
    old_img_params['width'] = old_img_params['size'][0]
    old_img_params['height'] = old_img_params['size'][1]
    old_img_params['ratio'] = img_object.size[0] / img_object.size[1]
    return old_img_params


def create_new_image_name(
        default_name,
        extension,
        new_size,
        width=None,
        height=None,
        newname=None,
        scale=None
    ):
    short_name_template = '{}{}'.format(newname, extension)
    long_name_template = '{}__{}x{}{}'.format(
        default_name,
        new_size.width,
        new_size.height,
        extension
    )
    if scale:
        if newname is not None:
            full_newname = short_name_template
        else:
            full_newname = long_name_template
    if any([width, height]):
        if newname is not None:
            full_newname = short_name_template
        else:
            full_newname = long_name_template
    return full_newname


def create_savepath(newname, directory):
    if (directory and newname) or directory:
        savepath = join(directory, newname)
    elif newname and not directory:
        savepath = join(getcwd(), newname)
    return savepath


def built_new_size(
        old_size,
        old_ratio,
        width=None,
        height=None,
        scale=None
    ):
    new_size_params = {}
    size_tuple = namedtuple('size', 'width height')
    if width and not height:
        new_width = width
        new_height = int(width / old_ratio)
        new_size = size_tuple(new_width, new_height)
    elif height and not width:
        new_width = int(height * old_ratio)
        new_height = height
        new_size = size_tuple(new_width, new_height)
    elif width and height:
        new_size = size_tuple(width, height)
    elif scale:
        new_size = [int(scale * dimension) for dimension in old_size]
        new_size = size_tuple(new_size[0], new_size[1])
    new_ratio = new_size.width / new_size.height
    new_size_params['new_size'] = new_size
    new_size_params['new_ratio'] = new_ratio
    new_size_params['close_ratio'] = isclose(
        old_ratio,
        new_ratio,
        rel_tol=0.01)
    return new_size_params


def resize_image(
        img_object,
        new_name,
        new_size,
        savepath
    ):
    new_image = img_object.resize(new_size, Image.ANTIALIAS)
    new_width, new_height = new_size.width, new_size.height
    new_image.save(savepath)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.scale and any([args.width, args.height]):
        parser.error('Conflict: incompatible arguments!')
    if exists(args.filepath):
        path = args.filepath
        img_object = open_image(path)
        old_image_params = get_old_img_params(img_object, path)
        new_size_params = built_new_size(
            old_image_params['size'],
            old_image_params['ratio'],
            args.width,
            args.height,
            args.scale
        )
        new_image_name = create_new_image_name(
            old_image_params['name'],
            old_image_params['ext'],
            new_size_params['new_size'],
            args.width,
            args.height,
            args.newname,
            args.scale
        )
        savepath = create_savepath(new_image_name, args.newpath)
        resize_image(
            img_object,
            new_image_name,
            new_size_params['new_size'],
            savepath
        )
        print('\nNew image successfully saved.')
        if (args.width or args.height) and not new_size_params['close_ratio']:
            print('\nWarning! New ratio much differ from the original.')
