import math
import os
import subprocess

import moviepy.editor as mp
import numpy
from PIL import Image, ImageDraw, ImageFont
import sympy as sp
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from pydub import AudioSegment
from colorama import Fore, Back, Style
from colorama import init as color_init

from ascii_art_numbers import numbers as numbers
from caption import max_width as max_caption_width

size = (1920, 1080)
start_percentage = 75
end_percentage = 85
fps = 24

"""THIS INITIALIEZES THE COLOR THING"""
color_init()

black = Fore.BLACK
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
magenta = Fore.MAGENTA
cyan = Fore.CYAN
white = Fore.WHITE

def colorprint(color=None, text=None):
    text = str(text)
    print(color + text + Style.RESET_ALL)

def c_print(color = white, text=None):
    text = str(text)
    print(color + text + Style.RESET_ALL)
""""""

c_print(yellow, 'imported...')

def zoom_ratio(frame_number = 1, start_percentage=75, end_percentage = 85):
    diff_ratio = (end_percentage / start_percentage) - 1
    
    x = sp.symbols('x')
    eq = sp.Eq(((-1/x) + diff_ratio), 0)
    zero = sp.solve(eq, x)[0]
    
    multiplier = (-1/(frame_number + zero)) + diff_ratio
    multiplier = multiplier + 1
    
    return multiplier

def make_video(location, count):

    count = str(count)

    image = os.path.join(location, 'images', count + '.png')
    background = os.path.join(location, 'images', 'backgrounds', count + '.png')
    caption = os.path.join(location, 'images', 'captions', count + '.png')
    try: 
        audio_path = os.path.join(location, 'audio', count + '.mp3')
        audio = AudioFileClip(audio_path)
        audio_duration = (len(AudioSegment.from_file(audio_path)) / 1000)
        dodobool = True
    except:
        audio_duration = 5
        dodobool = False

    try:
        c_print(yellow, numbers[count] + '\n')
    except:
        pass

    ratio = 1
    blurred_img_obj = Image.open(background)
    img_obj = Image.open(image)
    caption_image_obj = Image.open(caption)

    frame_count = int(audio_duration * fps)
    c_print(green, str(frame_count) + ' frames ')

    new_frame = blurred_img_obj.copy()

    list_img_frames = []
    re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
    re_sized_image = img_obj.resize(re_size, Image.LANCZOS)

    new_frame.paste(caption_image_obj, (((1920 - max_caption_width) // 2), int((size[1] - ((size[1] * ((100 - end_percentage) / 100) / 2) + caption_image_obj.height)/2))), caption_image_obj.convert("RGBA")) # add caption
    new_frame_arr = numpy.array(new_frame)

    for frame in range(frame_count):
        frame = frame + 1
        new_re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
        if new_re_size[1] > re_size[1]:
            re_sized_image = img_obj.resize(new_re_size, Image.LANCZOS)
            re_size = new_re_size
            position = tuple(((s - r) // 2) for s, r in zip(size, re_size))
            new_frame.paste(re_sized_image, position, re_sized_image.convert("RGBA"))      #overlay image
            new_frame_arr = numpy.array(new_frame)

        list_img_frames.append(new_frame_arr)

        ratio = zoom_ratio(frame_number = (frame+1))

        c_print(red, f'image {frame} of {frame_count} made ')


    clip = ImageSequenceClip(list_img_frames, fps=fps)  
    if dodobool: 
        clip = clip.set_audio(audio)
    clip.write_videofile(os.path.join(location, 'subvideos', count + '.mp4'))

    c_print(cyan, f'video {count} made ')
        

#==============================================================================================================================================

                                    
def stitch_from_subvideos():
    subvideos_path_list = list(f'd:\\babel2\\videos\\subvideos\\{x}' for x in range(1,10))
    

def main():
    sub_videos_list = []

    final_clip = concatenate_videoclips(sub_videos_list)
    final_clip.write_videofile("final_output07.mp4") 

if __name__ == "__main__":
    main()