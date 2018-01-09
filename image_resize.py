import argparse
from os import getcwd
from os.path import basename, exists, join, splitext
from math import isclose
from PIL import Image


def create_parser():
    parser = argparse.ArgumentParser(prog='Image Resizer')
    parser.add_argument('filepath', help='Path to original image', type=str)
    parser.add_argument('--scale', help='Float, positive', type=float)
    parser.add_argument('--width', help='Integer, positive', type=int)
    parser.add_argument('--height', help='Integer, positive', type=int)
    parser.add_argument('--output', help='Where to save new image', type=str)
    parser.add_argument('--newname', help='New name without ext.', type=str)
    return parser


def open_image(path_to_original):
    return Image.open(path_to_original)


def rescale_image(img_obj, scale):
    new_size = tuple([int(scale * dimension) for dimension in img_obj.size])
    return img_obj.resize(new_size, Image.ANTIALIAS)


def resize_image_by_two_sizes(img_obj, new_width, new_height):
    return img_obj.resize((new_width, new_height), Image.ANTIALIAS)


def check_aspect_ratio_proximity(img_obj, new_width, new_height):
    old_ratio = img_obj.size[0] / img_obj.size[1]
    new_ratio = new_width / new_height
    return not isclose(old_ratio, new_ratio, rel_tol=0.05)


def resize_image_by_one_size(img_obj, new_width, new_height):
    old_width = img_obj.size[0]
    old_height = img_obj.size[1]
    if new_width:
        new_size = (new_width, int(new_width / old_width * old_height))
    if new_height:
        new_size = (int(new_height / old_height * old_width), new_height)
    return img_obj.resize(new_size, Image.ANTIALIAS)


def create_savepath(new_img_obj, path_to_original, output_dir, output_name):
    original_name = splitext(basename(path_to_original))[0]
    extention = splitext(basename(path_to_original))[1]
    short_template = '{}{}'.format(output_name, extention)
    long_template = '{}__{}x{}{}'.format(
        original_name,
        new_img_obj.size[0],
        new_img_obj.size[1],
        extention)
    if output_dir and output_name:
        savepath = join(output_dir, short_template)
    else:
        savepath = join(getcwd(), template)
    return savepath


def save_image(new_img_obj, savepath):
    new_img_obj.save(savepath)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if not exists(args.filepath):
        parser.error('File not found.')
    if args.scale and (args.width or args.height):
        parser.error('Conflict: incompatible arguments.')
    old_img = open_image(args.filepath)
    if args.width and args.height:
        new_img = resize_image_by_two_sizes(old_img, args.width, args.height)
    if all([
        args.width,
        args.height,
        check_aspect_ratio_proximity(old_img, args.width, args.height)
        ]):
            print('\nWarning! Resulting image may be distorted.')
    elif args.width or args.height:
        new_img = resize_image_by_one_size(old_img, args.width, args.height)
    elif args.scale:
        new_img = rescale_image(old_img, args.scale)
    savepath = create_savepath(
       new_img,
       args.filepath,
       args.output,
       args.newname
    )
    save_image(new_img, savepath)
    print('\nNew image successfully saved.')
