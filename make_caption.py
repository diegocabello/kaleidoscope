import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

from colorprint import colorprint

font_path = os.path.join('resources', 'fonts', 'EBGaramond-Medium.ttf')
white = (255, 255, 255)
black = (0,0,0)
transparent = (0,0,0,0)
max_width = 1536
font = ImageFont.truetype(font_path, 28)

def splitter(text):
    list_of_pairs = []
    two_pair = []
    words = text.split() # this is a list of words
    line = ''

    for word in words: 
        line_clone = line + word + ' '
        if font.getsize(line_clone)[0] < max_width:
            line = line + word + ' '
        else:
            two_pair.append(line)
            if len(two_pair) == 2:
                list_of_pairs.append(two_pair)
                two_pair = []
            line = word + ' '
    if line.strip(): # if there's still a remaining line
        two_pair.append(line.strip())
        list_of_pairs.append(two_pair)

    return list_of_pairs

def collapse(super_list):
    return_list = []
    for lister in super_list:
        if len(lister) == 2:
            return_list.append(lister[0] + ' ' + lister[1])
        else:
            return_list.append(lister[0])
    return return_list

def make_caption_plural(list_of_lines, file_name, font_color):

    file_name = str(file_name) + '.png' if not str(file_name).endswith('.png') else str(file_name)

    buffer = 4 # must be divisible by 2
    image_height = (font.getsize('h')[1] + buffer * 3) * len(list_of_lines)
    final_image = Image.new('RGBA', (max_width, image_height), color = transparent)

    height_index = 0
    for wrapped_line in list_of_lines:
        text_width, text_height = font.getsize(wrapped_line)[0], font.getsize(wrapped_line)[1]
        width_index = (max_width - text_width) // 2
        sub_image_height = text_height + buffer
        ImageDraw.Draw(final_image).text((width_index, height_index), wrapped_line, fill=font_color, font=font)
        height_index = height_index + sub_image_height

    final_image.save(file_name)

    return final_image

def make_caption(text, location, file_name):

    file_name=str(file_name)
    pair_counter = 0

    output_location_list = []

    if location: 
        output_location = os.path.join(location, 'images\\captions')
        component_location = os.path.join(location, 'images\\captions\\components')
    else: 
        output_location = os.path.join('images\\captions')
        component_location = os.path.join('images\\captions\\components')

    list_of_pairs = splitter(text)

    for pair in list_of_pairs:
        pair_counter += 1

        output_path = os.path.join(output_location, f'{file_name}_{str(pair_counter)}.png')
        white_file_name = os.path.join(component_location, f'{file_name}_{str(pair_counter)}_white.png')
        black_file_name = os.path.join(component_location, f'{file_name}_{str(pair_counter)}_black.png')
        black_boxblur_file_name = os.path.join(component_location, f'{file_name}_{str(pair_counter)}_black_boxblur.png')
        output_location_list.append(output_path)

        white_image = make_caption_plural(pair, white_file_name, white)
        black_image = make_caption_plural(pair, black_file_name, black)

        cmd = f'ffmpeg -i "{black_file_name}" -vf "boxblur=3" -frames:v 1 -loglevel error "{black_boxblur_file_name}"'
        subprocess.run(cmd, shell=True)
        blurred_black_image = Image.open(black_boxblur_file_name)

        final_image = Image.new('RGBA', white_image.size, color=transparent)
        final_image = Image.alpha_composite(final_image, blurred_black_image)
        final_image = Image.alpha_composite(final_image, white_image)

        final_image.save(output_path)

    colorprint('magenta', f'\tcaption {file_name} made ')

    return {"text": collapse(list_of_pairs), "locations": output_location_list}
