import os
import argparse
#from PIL import Image

def get_original_image_info(filepath):
    if os.path.exists(filepath):
        original_name = os.basename(filepath).split('.')[0]
        original_image = Image.open(filepath)
        original_format = original_image.format
        original_size = original_image.size
        original_width = original_size[0]
        original_height = original_size[1]
        original_ratio = original_width/original_height
        return original_image, original_name, original_format, original_size, original_ratio
    else:
        return None

def create_image_name(image_info, out_width = None, out_height = None, out_name = None):
    
    
    
    
        
        
def rescale_image(filepath, scale, savepath):
    new_image = original_image.resize([int(scale * dimension) for dimension in original_size], Image.ANTIALIAS)
    new_image.save()
    
    
    
def resize_image()
    
    

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
 
def main():
    arguments = creare_parser()
    image_info = get_original_image_info(arguments.filepath)
    
 
create_parser()
