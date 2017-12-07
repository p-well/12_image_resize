import os
import argparse
from math import isclose
from collections import namedtuple
from PIL import Image


def return_args():
    parser = argparse.ArgumentParser(prog='Image Resizer')
    parser.add_argument('filepath',
                        help='old image filepath', type=str)
    parser.add_argument('--scale',
                        help='Scale parameter: float, positive', type=float)
    parser.add_argument('--width',
                        help='New image width: integer, positive', type=int)
    parser.add_argument('--height',
                        help='New image height: integer, positive', type=int)
    parser.add_argument('--outdir',
                        help='Output directory path', type=str)
    parser.add_argument('--outname',
                        help='Output name of modified image. \
                        Do not specify file extension.', type=str)
    args = parser.parse_args()
    if args.scale and (args.width or args.height):
        exit('\nAgruments conflict! Do not combine --scale flag with\
--width or -- height flag. Run script again with correct arguments.')
    else:
        return args


def get_old_image_params(filepath):
    if os.path.exists(filepath):
        old_image_params = {}
        size_tuple = namedtuple('size','width height')
        image_object = Image.open(filepath)
        old_image_basename = os.path.basename(filepath)
        old_image_params['name'],\
        old_image_params['extension'] = os.path.splitext(old_image_basename)
        old_image_params['image_object'] = image_object
        old_img_size = size_tuple(image_object.size[0], image_object.size[1])
        old_image_params['size'] = old_img_size
        old_image_params['width'] = old_img_size.width
        old_image_params['height'] = old_img_size.height
        old_image_params['ratio'] = (old_img_size.width / old_img_size.height)
        return old_image_params
    else:
        return None


def create_new_image_name(default_name,
                          extension,
                          new_size,
                          width=None,
                          height=None,
                          name=None,
                          scale=None
                          ):
    short_name_template = '{}.{}'.format(name, extension)
    long_name_template = '{}__{}x{}.{}'.format(default_name,
                                               new_size.width,
                                               new_size.height,
                                               extension)
    if scale:
        if name is not None:
            new_image_name = short_name_template
        else:
            new_image_name = long_name_template
    if (width or height):
        if name is not None:
            new_image_name = short_name_template
        else:
            new_image_name = long_name_template
    return new_image_name


def create_savepath(name, directory):
    if (directory and name) or directory:
        savepath = os.path.join(directory, name)
    elif name and not directory:
        savepath = os.path.join(os.getcwd(), name)
    return savepath


def built_new_size(old_size,
                   old_ratio,
                   width=None,
                   height=None,
                   scale=None
                   ):
    new_size_params = {}
    size_tuple = namedtuple('size','width height')
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
    new_size_params['ratios_promixity'] = isclose(old_ratio,
                                                new_ratio,
                                                rel_tol=0.01)
    return new_size_params


def rescale_image(old_image_object,
                  new_name,
                  new_size,
                  savepath
                  ):
    new_image = old_image_object.resize(new_size, Image.ANTIALIAS)
    new_image.save(savepath)


def resize_image(old_image_object,
                 new_name,
                 new_size,
                 savepath
                 ):
    new_image = old_image_object.resize(new_size, Image.ANTIALIAS)
    new_width, new_height = new_size.width, new_size.height
    new_image.save(savepath)


def main():
    arguments = return_args()
    old_image_params = get_old_image_params(arguments.filepath)
    new_size_params = built_new_size(old_image_params['size'],
                                     old_image_params['ratio'],
                                     arguments.width,
                                     arguments.height,
                                     arguments.scale)
    new_image_name = create_new_image_name(old_image_params['name'],
                                           old_image_params['extension'],
                                           new_size_params['new_size'],
                                           arguments.width,
                                           arguments.height,
                                           arguments.outname,
                                           arguments.scale)
    savepath = create_savepath(new_image_name,
                               arguments.outdir)
    if arguments.scale:
        rescale_image(old_image_params['image_object'],
                      new_image_name,
                      new_size_params['new_size'],
                      savepath)
    elif arguments.width or arguments.height:
        if not new_size_params['ratios_promixity']:
            print('\nWarning! New aspect ratio much differ from the original')
        resize_image(old_image_params['image_object'],
                     new_image_name,
                     new_size_params['new_size'],
                     savepath)


if __name__ == '__main__':
    main()
