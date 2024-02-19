import math
import os
import subprocess
import sys

import moviepy.editor as mp
import numpy
from PIL import Image, ImageDraw, ImageFont
import sympy as sp
import math
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
from pydub import AudioSegment
from colorama import Fore, Style
from colorama import init as color_init

from colorprint import colorprint
from ascii_art_numbers import numbers as numbers
from make_caption import max_width as max_caption_width
from resources.create_resources import padding

size = (1920, 1080)
start_percentage = 75
end_percentage = 85
fps = 24

"""THIS INITIALIZES THE COLOR"""
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
""""""

def caption_coords_function(caption):
    to_branch_from = (size[1] * ((100 - end_percentage) / 2 ) / 100)    # determines proportionally where to put the caption 
    other_expendature = (size[1] - to_branch_from) + (to_branch_from / 2)
    capt_cushion = (caption.height / 2)                       # adds half the caption height to it to center it 
    capt_height_coord = int(other_expendature - capt_cushion)
    capt_width_coord = int((size[0] - max_caption_width) // 2)
    return (capt_width_coord, capt_height_coord)

def zoomer_ratio(frame_number = 1, start_percentage=75, end_percentage = 85):
    diff_ratio = (end_percentage / start_percentage) - 1
    
    x = sp.symbols('x')
    eq = sp.Eq(((-1/x) + diff_ratio), 0)
    zero = sp.solve(eq, x)[0]
    
    multiplier = (-1/(frame_number + zero)) + diff_ratio
    multiplier = multiplier + 1
    
    return multiplier

def make_zoom_in_video(location, file_name, audio_paths = [], caption_paths = [], zoom_ratio=0.022, fps=fps):
    file_name = str(file_name)
    frame_counter = 0

    # declare
    image = os.path.join(location, 'images', file_name + '.png')
    background = os.path.join(location, 'images', 'backgrounds', file_name + '.png')
    shadow = r'resources\shadow_blurred.png'
    img_obj, shadow_obj = Image.open(image), Image.open(shadow) # intial create objects

    # handle audio
    audio_data = []
    for audio_path in audio_paths:
        to_append = {}
        to_append["audio path"] = audio_path
        to_append["length in frames"] = (len(AudioSegment.from_file(audio_path)) * fps // 1000) 
        audio_data.append(to_append)
    concatenated_audio = concatenate_audioclips([AudioFileClip(dicto["audio path"]) for dicto in audio_data])
    #total_duration = concatenated_audio.duration
    total_duration = sum([dicto["length in frames"] for dicto in audio_data]) / 24
    colorprint('magenta', total_duration)

    # handle captions 
    caption_data = []
    for caption in caption_paths: 
        to_append = {}
        caption_image = Image.open(caption)
        to_append["image"] = caption_image
        to_append["coords"] = caption_coords_function(caption_image)
        caption_data.append(to_append)

    caption_obj = caption_data[0]["image"]
    caption_coords = caption_coords_function(caption_obj)

    print(caption_data)
    print(audio_data)

    # initialize counters 
    ratio = 1
    complex_print = False
    change_fram_count = 0
    a_c_pair_counter = 0
    fram_count = int(total_duration * fps)
    more_than_frame_counter = audio_data[0]["length in frames"]

    # where things start + how big they are
    shadow_size = shadow_obj.size
    re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
    shadow_re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in shadow_size)
    position = re_size
    shadow_position = tuple(int(x - padding * ratio * (start_percentage/100)) for x in position)
    re_sized_image = img_obj.resize(re_size, Image.LANCZOS)
    re_sized_shadow = shadow_obj.resize(shadow_re_size, Image.LANCZOS)

    colorprint("green", '\t' + str(fram_count) + ' frames ')

    def effect(get_frame, t):
        nonlocal frame_counter, position, complex_print, re_sized_image, re_sized_shadow, shadow_position, ratio, re_size, change_fram_count, shadow_obj, a_c_pair_counter, caption_obj, caption_coords, more_than_frame_counter

        frame_counter += 1

        # RESIZE AND DECLARE BACKGROUND IMAGE
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_background_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        new_background_size[0] = new_background_size[0] + (new_background_size[0] % 2)
        new_background_size[1] = new_background_size[1] + (new_background_size[1] % 2)

        img = img.resize(new_background_size, Image.LANCZOS)

        x = math.ceil((new_background_size[0] - base_size[0]) / 2)
        y = math.ceil((new_background_size[1] - base_size[1]) / 2)

        img = img.crop([x, y, new_background_size[0] - x, new_background_size[1] - y]).resize(base_size, Image.LANCZOS)

        # RESIZE FOREGROUND IMAGE AND SHADOW 
        if frame_counter != 1: 
            new_foreground_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
            new_shadow_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in shadow_size)
            if new_foreground_size[1] > re_size[1]:
                re_size = new_foreground_size
                complex_print = True
                change_fram_count += 1

                re_sized_image = img_obj.resize(new_foreground_size, Image.LANCZOS) # resize image 
                re_sized_shadow = shadow_obj.resize(new_shadow_size, Image.LANCZOS)
                position = tuple(((s - r) // 2) for s, r in zip(size, re_size))
                shadow_position = tuple(int(x - padding * ratio * (start_percentage/100)) for x in position)

        # PASTE 
        img.paste(re_sized_shadow, shadow_position, re_sized_shadow.convert("RGBA")) # shadow
        img.paste(re_sized_image, position, re_sized_image.convert("RGBA"))      # image

        if frame_counter >= more_than_frame_counter:
            if not (a_c_pair_counter + 1) == len(audio_data):
                a_c_pair_counter += 1 
            more_than_frame_counter += audio_data[a_c_pair_counter]["length in frames"]
            caption_obj = caption_data[a_c_pair_counter]["image"]
            caption_coords = caption_coords_function(caption_obj)
        
        img.paste(caption_obj, caption_coords, caption_obj.convert("RGBA")) # caption

        # PRINT TO COMMAND LINE 
        if frame_counter % 10 == 0 or frame_counter == 1:
            if complex_print:
                print('\t' + red + 'new image ' + cyan + str(change_fram_count).zfill(2) + red + ' at frame ' + yellow + str(frame_counter).zfill(2) + red + ' of ' + green + str(fram_count) + reset)
            else:
                print('\t' + red + 'made frame ' + yellow + str(frame_counter).zfill(2) + red + ' of ' + green + str(fram_count) + reset)
        elif complex_print:
            print('\t' + red + 'new image ' + cyan + str(change_fram_count).zfill(2) + red + ' at frame ' + green + str(frame_counter).zfill(2) + red + ' of ' + green + str(fram_count) + reset)

        complex_print = False
        ratio = zoomer_ratio(frame_number = frame_counter)

        # CLOSE
        result = numpy.array(img)
        img.close()

        return result

    return mp.ImageClip(background).set_fps(fps).set_duration(total_duration).resize(size).fl(effect).set_audio(concatenated_audio) 

def make_video(location, file_name, audio_paths, caption_paths):

    save_path = os.path.join(location, 'subvideos', str(file_name) + '.mp4')
    make_zoom_in_video(location, file_name, audio_paths, caption_paths).write_videofile(save_path, fps=24, verbose=False) 

#==============================================================================================================================================

def make_video_depriciated(location, count):

    # DECLARE EVERYTHING 
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
        colorprint(yellow, numbers[count] + '\n')
    except:
        pass

    ratio = 1
    complex_print = False

    blurred_image_obj, img_obj, caption_image_obj = Image.open(background), Image.open(image), Image.open(caption) # intial create objects
    caption_coords = caption_coords_function(caption_image_obj)

    re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)
    re_sized_image = img_obj.resize(re_size, Image.LANCZOS)

    change_fram_count = 0
    fram_count = int(audio_duration * fps)
    colorprint(green, str(fram_count) + ' frames ')

    #.paste(caption_image_obj, caption_coords, caption_image_obj.convert("RGBA")) # add caption

    list_img_frames = []
    list_of_background_frames = make_zoom_in_video(background, 5)

    # EACH FRAME 
    for frame_counter, frame in enumerate(list_of_background_frames):
        frame_counter += 1
        change_fram_count += 1

        new_re_size = tuple((new_size := math.ceil(x * (start_percentage/100) * ratio)) + (new_size % 2) for x in size)

        if new_re_size[1] > re_size[1] and frame_counter != 1:
            re_size = new_re_size
            re_sized_image = img_obj.resize(new_re_size, Image.LANCZOS) # resize image 
            position = tuple(((s - r) // 2) for s, r in zip(size, re_size))
            frame.paste(re_sized_image, position, re_sized_image.convert("RGBA"))      # overlay image
            #frame.paste(caption_image_obj, caption_coords, caption_image_obj.convert("RGBA")) # add caption1
            complex_print = True

        if frame_counter % 10 == 0 or frame_counter == 1:
            if complex_print:
                print('\t' + red + 'new image ' + magenta + str(change_fram_count).zfill(2) + red + ' at frame ' + green + str(frame).zfill(2) + red + ' of ' + green + str(fram_count) + reset)
            else:
                print('\t' + red + 'made frame ' + yellow + str(frame_counter).zfill(2) + red + ' of ' + green + str(fram_count) + reset)
        elif complex_print:
            print('\t' + red + 'new image ' + cyan + str(change_fram_count).zfill(2) + red + ' at frame ' + green + str(frame).zfill(2) + red + ' of ' + green + str(fram_count) + reset)

        complex_print = False

        list_img_frames.append(numpy.array(frame))
        ratio = zoom_ratio(frame_number = (frame_counter))

    print(red + 'frame ' + green + str(fram_count) + red + ' of ' + green + str(fram_count) + reset)

    clip = ImageSequenceClip(list_img_frames, fps=fps) 
 
    if dodobool: 
        clip = clip.set_audio(audio)
    clip.write_videofile(os.path.join(location, 'subvideos', count + '.mp4'))

    colorprint(cyan, f'video {count} made ')
        
#==============================================================================================================================================


if __name__ == "__main__":
    make_zoom_in_video(r'D:\babel\dracula', 1, 5).write_videofile('zoomin4.mp4', fps=24, verbose=False)
    subprocess.run(r'zoomin4.mp4', shell=True)
