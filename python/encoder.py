from clrprint import clrprint
import urllib.request
import numpy as np
import sys

import cv2 as cv
import argparse
import json
import PIL

OPTIONS = {}

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

def show_image(image):
    if image is None:
        raise Exception("Image can't be none.")
    if type(image) is PIL.Image.Image:
        image.show()
        return
    cv.imshow("image", resize(image, 500))
    
    cv.waitKey(0)
    cv.destroyAllWindows()

def resize(image, size):
    if image is None:
        raise Exception("Image can't be none.")
    height, width, *_ = image.shape
    w, h = int(width * (size / height)), size
    if width > height:
        w, h = size, int(height * (size / width))
    return cv.resize(image, (w, h))

def get_properties():
    with open('meta/properties.json') as f:
        properties = json.load(f)
        properties['options'] = ''
        for option in OPTIONS:
            properties['options'] += f" - `{option}` {OPTIONS[option]['meta']}\n"
        properties['options'] = properties['options'][:-1]
        return properties

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

def init_cli():
    parser = argparse.ArgumentParser()
    options = list(OPTIONS.keys())
    
    parser.add_argument('--process', '-p', choices=options)
    parser.add_argument('--url', '-u')
    args = parser.parse_args()

    path = "https://cdn.dotmaui.com/ph/?size=250x251&bg=FF0000&color=FFCC00" if args.url is None else args.url
    image = get_image(path)
    
    if args.process != None:
        image = OPTIONS[args.process]['method'](image, 'data.txt')
        show_image(image)
        sys.exit()
        
    clrprint("[", "Argument Error", "] No process specified", sep="", clr="w,r,w")