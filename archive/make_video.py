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

reset = Style.RESET_ALL

def color_print(color = white, text=None):
    text = str(text)
    print(color + text + reset)
""""""

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
        color_print(yellow, numbers[count] + '\n')
    except:
        pass

    ratio = 1
    multiplier = 1
    complex_print = False

    blurred_image_obj, img_obj, caption_image_obj = Image.open(background), Image.open(image), Image.open(caption) # intial create objects
    print(blurred_image_obj)

    re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
    re_sized_image = img_obj.resize(re_size, Image.LANCZOS)

    to_branch_from = (size[1] * ((100 - end_percentage) / 2 ) / 100)    # determines proportionally where to put the caption 
    other_expendature = (size[1] - to_branch_from) + (to_branch_from / 2)
    capt_cushion = (caption_image_obj.height / 2)                       # adds half the caption height to it to center it 
    capt_height_coord = int(other_expendature - capt_cushion)
    capt_width_coord = int((size[0] - max_caption_width) // 2)
    caption_coords = (capt_width_coord, capt_height_coord)

    list_img_frames = []
    change_frame_count = 0
    frame_count = int(audio_duration * fps)
    color_print(green, str(frame_count) + ' frames ')

    #.paste(caption_image_obj, caption_coords, caption_image_obj.convert("RGBA")) # add caption

    for frame in range(frame_count):
        frame += 1
        change_frame_count += 1

        copied_background = blurred_image_obj.copy().resize(size, Image.LANCZOS)

        new_re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)

        if frame != 1:
            multiplier = multiplier * 1.002
            background_re_size = tuple(int(x * multiplier) for x in size)
            background_re_size = tuple(x + 1 if x % 2 == 1 else x for x in background_re_size)
            copied_background = copied_background.resize(background_re_size, Image.LANCZOS) # resize background
            diff_x = (background_re_size[0] - size[0]) // 2
            diff_y = (background_re_size[1] - size[1]) // 2
            crop_here = (diff_x, diff_y, (background_re_size[0] - diff_x), (background_re_size[1] - diff_y))
            copied_background = copied_background.crop(crop_here).resize(size, Image.LANCZOS)
            color_print(cyan, str(copied_background.size))

            copied_background = copied_background.paste(caption_image_obj, caption_coords, caption_image_obj.convert("RGBA")) # add caption 
            print('\n')
        else:
            #copied_background.paste(caption_image_obj, caption_coords, caption_image_obj.convert("RGBA")) # add caption
            copied_background.paste(img_obj, re_size, img_obj.convert("RGBA"))      # overlay image
            color_print(cyan, str(copied_background.size))


        """
        if new_re_size[1] > re_size[1] and frame != 1:
            re_sized_image = img_obj.resize(new_re_size, Image.LANCZOS) # resize image 
            re_size = new_re_size
            position = tuple(((s - r) // 2) for s, r in zip(size, re_size))
            copied_background.paste(re_sized_image, position, re_sized_image.convert("RGBA"))      # overlay image
            complex_print = True
        """

        new_frame_arr = numpy.array(copied_background)

        if frame % 10 == 0 or frame == 1:
            if complex_print:
                print('\t' + red + 'new image ' + cyan + str(change_frame_count).zfill(2) + red + ' at frame ' + green + str(frame).zfill(2) + red + ' of ' + green + str(frame_count) + reset)
            else:
                print('\t' + red + 'made frame ' + yellow + str(frame).zfill(2) + red + ' of ' + green + str(frame_count) + reset)
        elif complex_print:
            print('\t' + red + 'new image ' + green + str(change_frame_count).zfill(2) + red + ' at frame ' + green + str(frame).zfill(2) + red + ' of ' + green + str(frame_count) + reset)

        complex_print = False

        list_img_frames.append(new_frame_arr)
        ratio = zoom_ratio(frame_number = (frame+1))

    print(red + 'frame ' + green + str(frame_count) + red + ' of ' + green + str(frame_count) + reset)

    clip = ImageSequenceClip(list_img_frames, fps=fps)  
    if dodobool: 
        clip = clip.set_audio(audio)
    clip.write_videofile(os.path.join(location, 'subvideos', count + '.mp4'))

    color_print(cyan, f'video {count} made ')
        
#==============================================================================================================================================

def main():
    sub_videos_list = []

    final_clip = concatenate_videoclips(sub_videos_list)
    final_clip.write_videofile("final_output07.mp4") 

if __name__ == "__main__":
    main()