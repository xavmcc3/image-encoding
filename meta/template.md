![image](../src/banner.png)

# <image src="../src/logo.png" width=37 style="vertical-align: middle;"> Image Encoding

Yoo this is a sick python program to encode images. 🥵🥵

## Installation

Just clone the repo, dawg. The full command is `git clone https://github.com/xavmcc3/image-encoding.git`. Then `cd` into the folder and run it. You could build it too, actually if you have PyInstaller but i'll update that later.

## Usage

Run it with `python main.py -p <process> -u <url>`, where `<process>` is the type of encoding to use and `<url>` is the url to the image. The options are below in case you don't wanna read the code.

{! options !}

Any output is stored in `data.txt` in the same directory.

## About
Honestly I'm pretty proud of this shit 'cause it uses cool-ass python decorator functions so if I wanna add an encoding type I can just be like 
```py
@process('description')
def shitty_process():
    pass
```
and it automatically adds it to `README.md`. The way I did that was pretty sick too low key. It takes a bunch of parameters in a dictionary and replaces them based off name so I can just add more variables to the file n shit.

## Todo
List of things I wanna add or change with this project. Lowkey the architexture kinda slaps.
 - [ ] Automatically hide this part of the readme if there's nothing there
 - [ ] render the ascii image to some sort of canvas (probably with PIL)
 - [ ] file inputs ? i guess?? kinda cringe tho
 - [ ] Cmd option for custom output filenames

© {! name !}, 2023 👍