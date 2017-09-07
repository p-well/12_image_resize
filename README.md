# Image Resizer

Scale flag can not be combined with width or height flags!
                                                 Single width or height flag will create image with aspect ratio 
                                                 similar to original.
                                                 Simultaneous usage of width and height flags will raise warning in case of
                                                 new aspect ratio is much differ from the original one, but new image
                                                 still will be created.


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --width 800

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --height 400

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --width 700 --height 400

Warning! New aspect ratio much differ from the original.

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --widht 460 --height 240 --outdir  C:\projects\devman --outname test_image1
usage: Image Resizing Program [-h] [--scale SCALE] [--width WIDTH]
                              [--height HEIGHT] [--outdir OUTDIR]
                              [--outname OUTNAME]
                              filepath
Image Resizing Program: error: unrecognized arguments: --widht 460

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --width 460 --height 240 --outdir  C:\projects\devman --outname test_image1

Warning! New aspect ratio much differ from original.

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --width 480  --outdir  C:\projects\devman --outname test_image2

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --height 320  --outdir  C:\projects\devman --outname test_image3

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --scale 1.2  --outdir  C:\projects\devman --outname test_image4

(env) c:\projects\devman\12_image_resize>python image_resize.py C:\projects\devman\12_image_resize\snapshot.jpg --scale 0.85  --outdir  C:\projects\devman

(env) c:\projects\devman\12_image_resize>

































