from python.encoder import process, init_cli, resize
import cv2 as cv
import sys
import os

from PIL import Image, ImageDraw, ImageFont
import numpy as np

#region utils
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
#endregion

#region processes
@process("Convert the image to pure black or pure white binary.")
def threshold_image(image, out, threshold=190, readable=True):
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
def ascii_image(image, out, print_data=True):
    image = image.copy()
    size = os.get_terminal_size()
    image = resize_for(image, (size.columns, size.lines - 1))
    
    pixel_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    height, width, *_ = image.shape
    output_data = ""
    
    
    
    target_font_size = 20
    w, h = width, height
    target_size = 0
    font_size = 0
    if w > h:
        target_size = target_font_size * w
        h = int(target_size / w * h)
        font_size = h / height
        w = target_size
    else:
        target_size = target_font_size * h
        w = int(target_size / h * w)
        
        font_size = w / width
        h = target_size
        
    # print(width, height)
    # print(w, h)
    # print(target_size)
    # print(font_size)
    
    result = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ctx = ImageDraw.Draw(result)
    
    font_size = int(font_size)
    font = ImageFont.truetype('fonts/Cascadia.ttf', font_size)
    
    def square(x, y, w):
        # ctx.rectangle((x, y, x + w, y + w), fill="#00000000", outline='#ffffff33', width=1)
        return (x, y, x + w, y + w)
    
    for y in range(height):
        for x in range(width):
            brightness = int(sum(image[y, x]) / len(image[y, x]) / 255 * (len(pixel_map) - 1))
            output_data += f"\x1b[38;2;{image[y, x][2]};{image[y, x][1]};{image[y, x][0]}m{pixel_map[brightness]} "
            
            color = (image[y, x][2], image[y, x][1], image[y, x][0])
            bounds = square(x / width * w, y / height * h, font_size)
            # ctx.text((bounds[0], bounds[1]), pixel_map[brightness], font=font, fill=color)
            _, _, t_w, t_h = ctx.textbbox((0, 0), "0", font=font)
            ctx.text((bounds[0] + t_w, bounds[1] + t_h / 2), pixel_map[brightness], font=font, fill=color, anchor='mm')
        output_data += "\n"
    output_data = output_data[:-1] + '\033[0m'
    
    # square(0, 0, font_size, (0, 190, 230))
    # square(w - font_size, h - font_size, font_size, (0, 190, 230))
    
    out.write(output_data)
    if print_data:
        sys.stdout.write(output_data)
        print()
    
    return result

@process('Convert the image to black and white with greyscale values.')
def grey_hex_image(image, out, readable=True):
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
    init_cli()