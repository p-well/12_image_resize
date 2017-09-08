# Image Resizer

CLI program for resing images by scale or dimenions.
Based on Pillow module - [pypi.python.org/pypi/Pillow/](https://pypi.python.org/pypi/Pillow/)


# Installation

Python 3.5 should be already installed. <br />
Clone this repo on your machnine and install dependencies using ```pip install -r requirements.txt``` in CLI. <br />
It is recommended to use virtual environment.


# Usage

To the script execute the following command in CLI: ```python image_resize <arguments>```

**Available arguments:**

-h --help:  show help

**Required arguments:**

filepath:  path to image you want to modify

**Optional arguments:**

--scale:  scale parament (positive, float)

--width:  new image width (positive, integer)

--y_height:  new image height (positive, integer)

--outpath:  new image output directory path

--outname:  new image name (without extentions) 

**Instructions:**

- Scale flag can not be combined with width or height flags!

- Usage of single width or height flag will create image with aspect ratio similar to original

- Simultaneous usage of width and height flags will raise warning in case of new aspect ratio
  is much differ (>5%) from the original one, but new image still will be created
  
- When one of flags --outpath or --outname is not specified the new image will be saved near original image (pic.jpg)
  with the following naming rule: ```pic__(new_width x new_height).jpg```

- The script does not change image type

# Example of Script Launch

```
>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --width 700 --height 400

Warning! New aspect ratio much differ from the original.
```


```
>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --scale 1.2 --outdir C:\projects\devman --outname test_image4
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
