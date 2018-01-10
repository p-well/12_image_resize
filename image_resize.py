import argparse
from os.path import basename, exists, splitext
from math import isclose
from PIL import Image


def create_parser():
    parser = argparse.ArgumentParser(prog='Image Resizer')
    parser.add_argument('filepath', help='Path to original image', type=str)
    parser.add_argument('--scale', help='Float, positive', type=float)
    parser.add_argument('--width', help='Integer, positive', type=int)
    parser.add_argument('--height', help='Integer, positive', type=int)
    parser.add_argument('--output', help='Where to save new image', type=str)
    return parser


def check_arguments(parser, args):
    if not exists(args.filepath):
        parser.error('File not found.')
    if args.scale and (args.width or args.height):
        parser.error('Conflict: incompatible arguments.')


def rescale_image(img_obj, scale):
    new_size = tuple([int(scale * dimension) for dimension in img_obj.size])
    return img_obj.resize(new_size, Image.ANTIALIAS)


def resize_image_by_two_sizes(img_obj, new_width, new_height):
    old_width, old_height = img_obj.size
    old_ratio = old_width / old_height
    new_ratio = new_width / new_height
    if not isclose(old_ratio, new_ratio, rel_tol=0.05):
        print('\nWarning! Resulting image may be distorted.')
    return img_obj.resize((new_width, new_height), Image.ANTIALIAS)


def resize_image_by_one_size(img_obj, new_width, new_height):
    old_width, old_height = img_obj.size
    if new_width:
        new_size = (new_width, int(new_width / old_width * old_height))
    if new_height:
        new_size = (int(new_height / old_height * old_width), new_height)
    return img_obj.resize(new_size, Image.ANTIALIAS)


def create_savepath(new_img_obj, path_to_original, output):
    original_name, extention = splitext(basename(path_to_original))
    new_width, new_height = new_img_obj.size
    short_template = '{}{}'.format(output, extention)
    long_template = '{}__{}x{}{}'.format(
        original_name,
        new_width,
        new_height,
        extention)
    if output:
        savepath = short_template
    else:
        savepath = long_template
    return savepath


def save_image(new_img_obj, savepath):
    new_img_obj.save(savepath)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    old_img = Image.open(args.filepath)
    check_arguments(parser, args)
    if args.width and args.height:
        new_img = resize_image_by_two_sizes(old_img, args.width, args.height)
    elif args.width or args.height:
        new_img = resize_image_by_one_size(old_img, args.width, args.height)
    elif args.scale:
        new_img = rescale_image(old_img, args.scale)
    savepath = create_savepath(new_img, args.filepath, args.output)
    save_image(new_img, savepath)
    print('\nNew image successfully saved.')
