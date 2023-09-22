from python.encoder import process, init_cli, resize
import cv2 as cv
import sys
import os

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
    init_cli()