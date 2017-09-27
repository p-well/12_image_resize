import os
import argparse
from PIL import Image
from math import isclose

def return_args():
    parser = argparse.ArgumentParser(prog = 'Image Resizing Program',
                                     description = 'CLI script for image resizing by scale or dimensions',
                                     epilog = 'See README for detailed program launch description')
    parser.add_argument('filepath', help = 'old image filepath', type=str)
    parser.add_argument('--scale', help = 'Scale parameter: float, positive value', type=float)
    parser.add_argument('--width', help = 'New image width: integer, positive value', type=int)
    parser.add_argument('--height', help = 'New image height: integer, positive value', type=int)
    parser.add_argument('--outdir', help ='Output directory path', type=str)
    parser.add_argument('--outname', help ='Output name of modified image.\
                                            Do not specify file extension.', type=str)
    args = parser.parse_args()
    return args

def get_old_image_info(filepath):
    if os.path.exists(filepath):
        old_image_info = {}
        old_image_info['name'] = os.path.basename(filepath).split('.')[0]
        old_image_info['extension'] = os.path.basename(filepath).split('.')[1]
        old_image_info['opened_image'] = Image.open(filepath)
        old_image_info['size'] = Image.open(filepath).size
        old_image_info['width'] = Image.open(filepath).size[0]
        old_image_info['height'] = Image.open(filepath).size[1]
        old_image_info['ratio'] = Image.open(filepath).size[0] / Image.open(filepath).size[1]
        return old_image_info
    else:
        return None

def create_outpath(outdir, outname): 
    if outdir and outname:
        out_basename = '{}.{}'.format(return_args().outname, 
                                      get_old_image_info(return_args().filepath).get('extension'))
        savepath = os.path.join(return_args().outdir, out_basename)
        return savepath

def create_new_image_name(out_width = None, out_height = None, out_dir = None, out_name = None):
    name = get_old_image_info(return_args().filepath).get('name')
    extension = get_old_image_info(return_args().filepath).get('extension')
    if not (out_dir and out_name):
        new_image_name = '{}__{}x{}.{}'.format(name, out_width, out_height, extension)
    else:
        new_image_name = '{}.{}'.format(out_name, extension)
    return new_image_name
        
def rescale_image(old_image_path, scale, out_path):
    old_size = get_old_image_info(return_args().filepath).get('size')
    old_image = get_old_image_info(return_args().filepath).get('opened_image')
    new_image = old_image.resize([int(scale * dimension) for dimension in old_size], Image.ANTIALIAS)
    new_width, new_height = new_image.size
    if (return_args().outdir and return_args().outname):
        new_image.save(out_path)
    else:    
        new_image.save(create_new_image_name(new_width, new_height))
    
def get_new_size(out_width = None, out_height = None):
    new_size_info = {}
    old_ratio = get_old_image_info(return_args().filepath).get('ratio')
    if out_width and not out_height:
        new_width = out_width
        new_height = int(out_width / old_ratio)
        new_size = new_width, new_height
    elif out_height and not out_width:
        new_width = int(out_height * old_ratio)
        new_height = out_height
        new_size = new_width, new_height
    else:
        new_size = out_width, out_height
    new_ratio = new_size[0] / new_size[1]
    new_size_info['new_size'] = new_size
    new_size_info['new_ratio'] = new_ratio
    new_size_info['ratios_promixity'] = isclose(old_ratio, new_ratio, rel_tol = 0.01) 
    return new_size_info 

def resize_image(old_image_path, size, out_path):
    old_image = get_old_image_info(return_args().filepath).get('opened_image')
    new_image = old_image.resize(size, Image.ANTIALIAS)
    new_width, new_height = size[0], size[1]
    if (return_args().outdir and return_args().outname):
        new_image.save(out_path)
    else:    
        new_image.save(create_new_image_name(new_width, new_height))

if __name__ == '__main__':           
    out_path = create_outpath(return_args().outdir, return_args().outname)
    if return_args().scale and (return_args().width or return_args().height):
        print('\nAgruments conflict! Use only --scale or --width and/or -- height flags.')
    elif return_args().scale:
        rescale_image(return_args().filepath, return_args().scale, out_path)
    elif return_args().width or return_args().height:
        if not get_new_size(return_args().width, return_args().height).get['ratios_promixity']:
            print('\nWarning! New aspect ratio much differ from old.')
        new_size = get_new_size(return_args().width, return_args().height).get['new_size']
        resize_image(return_args().filepath, new_size, out_path)
