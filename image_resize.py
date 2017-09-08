import os
import argparse
from PIL import Image
from math import isclose

def create_parser():
    parser = argparse.ArgumentParser(prog = 'Image Resizing Program',
                                     description = 'CLI script for image resizing by scale or dimensions',
                                     epilog = 'See README for detailed program launch description')
    parser.add_argument('filepath', help = 'Original image filepath', type=str)
    parser.add_argument('--scale', help = 'Scale parameter: float, positive value', type=float)
    parser.add_argument('--width', help = 'New image width: integer, positive value', type=int)
    parser.add_argument('--height', help = 'New image height: integer, positive value', type=int)
    parser.add_argument('--outdir', help ='Output directory path', type=str)
    parser.add_argument('--outname', help ='Output name of modified image.\
                                            Do not specify file extension.', type=str)
    args = parser.parse_args()
    return args

def get_original_image_info(filepath):
    if os.path.exists(filepath):
        original_name = os.path.basename(filepath).split('.')[0]
        original_extension = os.path.basename(filepath).split('.')[1]
        original_image = Image.open(filepath)
        original_size = original_image.size
        original_width = original_size[0]
        original_height = original_size[1]
        original_ratio = original_width / original_height
        return original_name, original_extension, original_size, original_ratio, original_image
    else:
        return None

def create_outpath(outdir, outname): 
    if outdir and outname:
        out_basename = '{}.{}'.format(args.outname, original_image_info[1])
        savepath = os.path.join(args.outdir, out_basename)
        return savepath

def create_new_image_name(out_width = None, out_height = None, out_dir = None, out_name = None):
    original_name = original_image_info[0]
    extension = original_image_info[1]
    if not (out_dir and out_name):
        new_image_name = '{}__{}x{}.{}'.format(original_name, out_width, out_height, extension)
    else:
        new_image_name = '{}.{}'.format(out_name, extension)
    return new_image_name
        
def rescale_image(original_image_path, scale, out_path):
    original_size = original_image_info[2]
    original_image = original_image_info[4]
    new_image = original_image.resize([int(scale * dimension) for dimension in original_size], Image.ANTIALIAS)
    new_width, new_height = new_image.size
    if (args.outdir and args.outname):
        new_image.save(out_path)
    else:    
        new_image.save(create_new_image_name(new_width, new_height))
    
def get_new_size(out_width = None, out_height = None):
    original_ratio = original_image_info[3]
    if out_width and not out_height:
        new_width = out_width
        new_height = int(out_width / original_ratio)
        new_size = new_width, new_height
    elif out_height and not out_width:
        new_width = int(out_height * original_ratio)
        new_height = out_height
        new_size = new_width, new_height
    else:
        new_size = out_width, out_height
    new_ratio = new_size[0] / new_size[1]     
    ratios_promixity = isclose(original_ratio, new_ratio, rel_tol = 0.01) 
    return new_size, ratios_promixity      

def resize_image(original_image_path, size, out_path):
    original_image = original_image_info[4]
    new_image = original_image.resize(size, Image.ANTIALIAS)
    new_width, new_height = size[0], size[1]
    if (args.outdir and args.outname):
        new_image.save(out_path)
    else:    
        new_image.save(create_new_image_name(new_width, new_height))

if __name__ == '__main__':
    args = create_parser()
    original_image_info = get_original_image_info(args.filepath)
    new_image_name = create_new_image_name(args.width, args.height, args.outdir, args.outname)
    out_path = create_outpath(args.outdir, args.outname)
    if args.scale and (args.width or args.height):
        print('\nAgruments conflict! Use only --scale or --width and/or -- height flags.')
    elif args.scale:
        rescale_image(args.filepath, args.scale, out_path)
    elif args.width or args.height:
        ratios_promixity = get_new_size(args.width, args.height)[1]
        if not ratios_promixity:
            print('\nWarning! New aspect ratio much differ from original.')
        new_size = get_new_size(args.width, args.height)[0]
        resize_image(args.filepath, new_size, out_path)
