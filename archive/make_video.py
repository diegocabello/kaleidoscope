import math
import os
import subprocess

import moviepy.editor as mp
import numpy
from PIL import Image, ImageDraw, ImageFont
import sympy as sp
import ffmpeg
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from pydub import AudioSegment
from colorama import Fore, Back, Style
from colorama import init as color_init

from ascii_art_numbers import numbers as numbers
from caption import max_width as max_caption_width

"""THESE ARE THE GLOBAL VARIABLES"""
size = (1920, 1080)
start_percentage = 75
fps = 24
""""""

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

"""THIS DEFINES THE CLASS AND MAKES ALL THE OBJECTS"""
class video_inputs:
    def __init__(self, image, blurred_image, audio, audio_duration, count, caption_image_path):
        self.image = image
        self.blurred_image = blurred_image
        self.audio = audio
        self.audio_duration = audio_duration
        self.count = count
        self.caption_image_path = caption_image_path
    

def sotr(number_clips=10):
    listo = []
    for x in range(1, number_clips + 1):
        audio_path = f"D:\\babel2\\audio\\{x}.mp3"
        thee_class = video_inputs(
            image = f"D:\\babel2\\images\\cropped\\{x}.png", 
            blurred_image = f"D:\\babel2\\images\\zoomed_and_blurred\\{x}.png", 
            audio = AudioFileClip(audio_path), 
            audio_duration = (len(AudioSegment.from_file(audio_path)) / 1000), # which is in seconds float
            count = x,
            caption_image_path = f"c:\\users\\diego\\documents\\my stuff\\programming stuff\\babel\\images\\captions\\{x-1}.png"
        )

        listo.append(thee_class)

    return listo
""""""

def zoom_ratio(frame_number = 1, start_percentage=75, end_percentage = 85):
    diff_ratio = (end_percentage / start_percentage) - 1
    
    x = sp.symbols('x')
    eq = sp.Eq(((-1/x) + diff_ratio), 0)
    zero = sp.solve(eq, x)[0]
    
    multiplier = (-1/(frame_number + zero)) + diff_ratio
    multiplier = multiplier + 1
    
    return multiplier


def make_sub_video(inputer = None):
    # unpack
    image = inputer.image
    blurred_img = inputer.blurred_image
    audio = inputer.audio
    audio_duration = inputer.audio_duration
    count = inputer.count
    caption_image_path = inputer.caption_image_path
    try:
        c_print(yellow, numbers[count] + '\n')
    except:
        pass

    ratio = 1
    blurred_img_obj = Image.open(blurred_img)
    img_obj = Image.open(image)
    caption_image_obj = Image.open(caption_image_path)

    frame_count = int(audio_duration * fps)
    c_print(green, str(frame_count) + ' frames ')

    new_frame = blurred_img_obj.copy()

    list_img_frames = []
    re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
    re_sized_image = img_obj.resize(re_size, Image.LANCZOS)

    new_frame.paste(overlay_image_obj, (0, 0),  overlay_image_obj.convert("RGBA"))    #darken background image
    new_frame.paste(caption_image_obj, (((1920 - max_caption_width) // 2), 1000), caption_image_obj.convert("RGBA")) # add caption

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
    clip = clip.set_audio(audio)
    clip.write_videofile(os.path.abspath(f'D:\\babel2\\video\\subvideos\\{count}.mp4'))

    c_print(cyan, f'video {count} made ')
    
    return clip


#if os.path.isfile('output.mp4'):                        # the output video 
#    os.remove('output.mp4')
                                    
def stitch_from_subvideos():
    subvideos_path_list = list(f'd:\\babel2\\videos\\subvideos\\{x}' for x in range(1,10))
    

def main():
    sub_videos_list = []
    list_of_objects = sotr()

    for object in list_of_objects:
        sub_videos_list.append(make_sub_video(inputer = object))

    final_clip = concatenate_videoclips(sub_videos_list)
    final_clip.write_videofile("final_output07.mp4") 

if __name__ == "__main__":
    main()