import os
import argparse
from PIL import Image

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

def create_new_image_name(out_width = None, out_height = None, out_dir = None, out_name = None):
    name = original_image_info[0]
    extension = original_image_info[1]
    if not (out_dir and out_name):
        new_image_name = '{}__{}x{}.{}'.format(name, out_width, out_height, extension)
    else:
        new_image_name = '{}.{}'.format(out_name, extension)
    return new_image_name
        
def rescale_image(original_image, scale, out_path): #out_path = outdir + outname + extension
    original_image = original_image_info[4]
    original_size = original_image_info[2]
    new_image = original_image.resize([int(scale * dimension) for dimension in original_size], Image.ANTIALIAS)
    new_width, new_height = new_image.size
    if (args.outdir and args.outname):
        new_image.save(out_path)
    else:    
        new_image.save(create_new_image_name(new_width, new_height))
    
def resize_image(original_image, out_width, our_height, out_path):


def create_parser():
    parser = argparse.ArgumentParser(prog = 'Image Resizing Program',
                                     description = 'CLI script for image resizing by scale or dimensions'
                                     epilog = '''Scale flag can not be combined with width or height flags!
                                                 Single width or height flag will create image with aspect ratio 
                                                 similar to original.
                                                 Simultaneous usage of width and height flags will raise warning in case of
                                                 new aspect ratio is much differ from the original one, but new image
                                                 still will be created.''')
    parser.add_argument('filepath', help = 'Original image filepath', type=str)
    parser.add_argument('--scale', help = 'Scale parameter: float, positive value', type=float)
    parser.add_argument('--width', help = 'New image width: integer, positive value', type=int)
    parser.add_argument('--height', help = 'New image height: integer, positive value', type=int)
    parser.add_argument('--outdir', help ='Output directory path', type=str)
    parser.add_argument('--outname', help ='Output name of modified image.\
                                            Do not specify file extension.', type=str)
    args = parser.parse_args()
    return args
 
if __name__ == '__main__':
    args = create_parser()
    original_image_info = get_original_image_info(args.filepath)
    new_image_name = create_new_image_name(args.width, args.height, args.outdir, args.outname)
    if args.scale and (args.width or args.height):
        print('Agruments conflict! Use only --scale or --width and/or -- height flags.')
    elif args.scale:
        extended_outname = '{}.{}'.format(args.outname, original_image_info[1])
        out_path = os.path.join(args.outdir, extended_outname)    
        rescale_image(args.filepath, args.scale, out_path)
       
