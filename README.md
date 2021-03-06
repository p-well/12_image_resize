# Image Resizer

This is console script for resizing images. Resize may be done in 2 ways - rescaling by scale factor or resizing <br />
using image dimensions.
Image handling in based on [Pillow](https://pypi.python.org/pypi/Pillow/) module.

Pavel Kadantsev, 2017. <br/>
p.a.kadantsev@gmail.com

# Installation

Python 3.5 should be already installed. <br />
Clone this repo on your machnine and install dependencies using ```pip install -r requirements.txt``` in CLI. <br />
It is recommended to use virtual environment.


# Usage

To execute the script use the following command in CLI: ```python image_resize.py <arguments>```

**Show available arguments:**

-h --help:  show help

**Required arguments:**

filepath:  path to image you want to modify

**Optional arguments:**

--scale:  scale parament (positive, float)

--width:  new image width (positive, integer)

--height:  new image height (positive, integer)

--output:  new image output path

**Instructions:**

- Scale flag can not be combined with width or height flags.

- Usage of single width or height flag will create image with aspect ratio similar to original.

- Simultaneous usage of width and height flags will raise warning in case of new aspect ratio
  is much differ (>5%) from the original one, but new image still will be created.
  
- When ```--output``` flag is not specified the new image will be saved near original image (pic.jpg)
  with the following naming rule: ```pic__(new_width x new_height).jpg```.
  
- The script does not change image type (i.e. file extention).

# Example of Script Launch


The following is an example of image resizing with sizes of 900 x 400, saved at one level folder higher ```..\``` with name ```plan```.

<pre>
<b> >python image_resize.py snapshot.JPG  --width 900 --height 400 --output ..\plan </b>

Warning! Resulting image may be distorted.

New image successfully saved.
</pre>


The following is an example of an error raised when agruments confict occured:

<pre>
<b> >python image_resize.py snapshot.JPG  --width 500 --scale 2 </b>
usage: Image Resizer [-h] [--scale SCALE] [--width WIDTH] [--height HEIGHT]
                     [--output OUTPUT] [--newname NEWNAME]
                     filepath
Image Resizer: error: Conflict: incompatible arguments.
</pre>


File not found error:

<pre>
<b>  c:\projects\devman\12_image_resize>python image_resize.py no_this_picture.JPG  --height 450 </b>
usage: Image Resizer [-h] [--scale SCALE] [--width WIDTH] [--height HEIGHT]
                     [--output OUTPUT] [--newname NEWNAME]
                     filepath
Image Resizer: error: File not found.
</pre>

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
