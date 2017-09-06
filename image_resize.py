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
        original_ratio = original_width/original_height
        return original_name, original_extension, original_size, original_ratio, original_image
    else:
        return None

def create_new_image_name(filepath, out_width = None, out_height = None, out_path = None, out_name = None):
    name, extension = original_image_info[0], original_image_info[1] 
    if not (out_path and out_name):
        new_image_name = '{}__{}x{}.{}'.format(name, out_width, out_height, extension)
    else:
        new_image_name = '{}.{}'.format(out_name, extension)
    return new_image_name
        
def rescale_image(filepath, scale, savepath):
    original_image, original_size = original_image_info[-1], original_image_info[2] 
    new_image = original_image.resize([int(scale * dimension) for dimension in original_size], Image.ANTIALIAS)
    new_image.save(new_image_name)
    
# #def resize_image()

def create_parser():
    parser = argparse.ArgumentParser(prog = 'Image Resize',
                                     description = 'CLI script for image resizing by scale or dimensions')
    parser.add_argument('filepath', help = 'Image filepath', type=str)
    parser.add_argument('--scale', help = 'Scale parameter: float, positive value', type=float)
    parser.add_argument('--width', help = 'New image width: integer, positive value', type=int)
    parser.add_argument('--height', help = 'New image height: integer, positive value', type=int)
    parser.add_argument('--outpath', help ='Output directory path', type=str)
    parser.add_argument('--outname', help ='Output name of modified image', type=str)
    arguments = parser.parse_args()
    return arguments
 
if __name__ == '__main__':
    arguments = create_parser()
    original_image_info = get_original_image_info(arguments.filepath)
    new_image_name = create_new_image_name(arguments.filepath,
                                        arguments.width,
                                        arguments.height,
                                        arguments.outname)
    rescale_image(arguments.filepath, arguments.scale, arguments.outpath)
