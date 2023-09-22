from meta.readme import update_readme

import urllib.request
import numpy as np
import sys
import os

from clrprint import clrprint
import cv2 as cv
import argparse

#region utils
def image_from_url(url):
    try:
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        return cv.imdecode(arr, -1)
    except urllib.error.HTTPError as e:
        clrprint("[", "URL Error", f"] {e}", sep="", clr="w,r,w")
        sys.exit()

def get_image(path, is_url=True):
    if is_url:
        max_url_len = 50
        url_str = path if len(path) < max_url_len else (path[:(max_url_len-3)] + '...')
        
        clrprint("Encoding ", "url", ":", url_str, sep="", clr="w,g,w,g")
        return image_from_url(path)
    
    clrprint("Encoding ", "file", ":", path, sep="", clr="w,g,w,g")
    return cv.imread(path)

def resize(image, size):
    if image is None:
        raise Exception("Image can't be none.")
    height, width, *_ = image.shape
    w, h = int(width * (size / height)), size
    if width > height:
        w, h = size, int(height * (size / width))
    return cv.resize(image, (w, h))

def resize_for(image, dims):
    if image is None:
        raise Exception("Image can't be none.")
    height, width, *_ = image.shape
    
    res_height = True
    size = dims[0]
    if dims[0] > dims[1]:
        res_height = False
        size = dims[1]
    
    w, h = int(width * (size / height)), size
    if res_height:
        w, h = size, int(height * (size / width))
    
    return cv.resize(image, (w, h))

def show_image(image):
    if image is None:
        raise Exception("Image can't be none.")
    cv.imshow("image", resize(image, 500))
    
    cv.waitKey(0)
    cv.destroyAllWindows()

def get_properties():
    properties = { 'name': 'Xav' }
    properties['options'] = ""
    for option in OPTIONS:
        properties['options'] += f" - `{option}` {OPTIONS[option]['meta']}\n"
    properties['options'] = properties['options'][:-1]
    return properties
#endregion

OPTIONS = {}
def process(metadata=""):
    def decorator(process):
        def wrapper(image, out_file, *args, **kwargs):
            with open(out_file, 'w') as out:
                height, width, *_ = image.shape
                clrprint("Dimensions are ", width, "x", height, sep="", clr="w,m,w,m,w")
                
                result = process(image, out, *args, **kwargs)
                clrprint("Wrote to '", out_file, "'", sep="", clr="w,b,w")
                return result
        OPTIONS[process.__name__] = {
            'method': wrapper,
            'meta': metadata
        }
        return wrapper
    return decorator

#region processes
@process("Convert the image to pure black or pure white binary.")
def threshold_process(image, out, threshold=190, readable=True):
    image = image.copy()
    image = resize(image, 500)
    
    end_char = ' ' if readable else ''
    height, width, *_ = image.shape
    
    for y in range(height):
        for x in range(width):
            image[y, x] = 255 if image[y, x][0] > threshold else 0
            out.write(f"{1 if image[y, x][0] > threshold else 0}{end_char}")
        if readable: out.write('\n')
    
    return image

@process('Convert the image to colored ascii characters.')
def ascii_process(image, out, print_data=True):
    image = image.copy()
    size = os.get_terminal_size()
    image = resize_for(image, (size.columns, size.lines - 1))
    
    pixel_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    height, width, *_ = image.shape
    output_data = ""
    
    for y in range(height):
        for x in range(width):
            brightness = int(sum(image[y, x]) / len(image[y, x]) / 255 * (len(pixel_map) - 1))
            output_data += f"\x1b[38;2;{image[y, x][2]};{image[y, x][1]};{image[y, x][0]}m{pixel_map[brightness]} "
        output_data += "\n"
    output_data = output_data[:-1] + '\033[0m'
    
    out.write(output_data)
    if print_data:
        sys.stdout.write(output_data)
        print()
    
    return image

@process('Convert the image to black and white with greyscale values.')
def hex_process(image, out, readable=True):
    image = image.copy()
    image = resize(image, 500)
    
    end_char = ' ' if readable else ''
    height, width, *_ = image.shape
    max_digits = 2
    
    max_val = 16 ** max_digits
    
    for y in range(height):
        for x in range(width):
            brightness = sum(image[y, x]) / len(image[y, x])
            image[y, x] = [brightness] * 3
            
            int_brightness = int(brightness / 255 * max_val)
            out.write(f"{str(hex(int_brightness))[2:]}{end_char}")
        if readable: out.write("\n")
    return image
#endregion


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = list(OPTIONS.keys())
    update_readme(get_properties())
    
    parser.add_argument('--process', '-p', choices=options)
    parser.add_argument('--url', '-u')
    args = parser.parse_args()

    path = "https://cdn.dotmaui.com/ph/?size=250x250&bg=FF0000&color=FFCC00" if args.url is None else args.url
    image = get_image(path)
    
    if args.process != None:
        image = OPTIONS[args.process]['method'](image, 'data.txt')
        
        show_image(image)
        exit()
        
    clrprint("[", "Argument Error", "] No process specified", sep="", clr="w,r,w")