import os
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageChops

from bigstringer import bigstringer
from colorprint import colorprint

font_path = os.path.join('resources', 'fonts', 'EBGaramond-Medium.ttf')
white = (255, 255, 255)
black = (0,0,0)
max_width = 1536
font = ImageFont.truetype(font_path, 32)


def make_caption_plural(text, file_name, font_color):

    file_name = str(file_name) + '.png' if not str(file_name).endswith('.png') else str(file_name)

    list_of_wrapped_lines = []
    words = text.split() #this is a list of words
    line = ''

    #this works but is not compact at all
    for word in words: 
        line_clone = line + word + ' '
        if font.getsize(line_clone)[0] < max_width:
            line = line + word + ' '
        else:
            list_of_wrapped_lines.append(line)
            line = word + ' '
        if word == words[-1]:
            list_of_wrapped_lines.append(line)     

    buffer = 4 # must be divisible by 2
    image_height = (font.getsize('h')[1] + buffer * 3) * len(list_of_wrapped_lines)
    final_image = Image.new('RGBA', (max_width, image_height), color = (0, 0, 0, 0))

    height_index = 0
    for wrapped_line in list_of_wrapped_lines:
        text_width, text_height = font.getsize(wrapped_line)[0], font.getsize(wrapped_line)[1]
        width_index = (max_width - text_width) // 2
        sub_image_height = text_height + buffer
        ImageDraw.Draw(final_image).text((width_index, height_index), wrapped_line, fill=font_color, font=font)
        height_index = height_index + sub_image_height

    final_image.save(file_name)

    return final_image

# I WANT TO TURN THIS INTO SVG LATER; actually i am not sure 
def make_caption(text, location, file_name):

    if location: 
        output_path = os.path.join(location, 'images\\captions', file_name)
    else: 
        output_path = os.path.join('images\\captions', file_name)

    white_file_name = str(output_path) + '_white.png'
    black_file_name = str(output_path) + '_black.png'
    black_blurred_file_name = str(output_path) + '_black_blurred.png' 
    white_image = make_caption_plural(text, white_file_name, white)
    black_image = make_caption_plural(text, black_file_name, black)

    cmd = f'ffmpeg -i {black_file_name} -vf "boxblur=1" -frames:v 1 -loglevel warning "{black_blurred_file_name}"'
    subprocess.run(cmd, shell=True)
    blurred_black_image = Image.open(black_blurred_file_name)

    final_image = Image.new('RGBA', white_image.size, color = (0, 0, 0, 0))
    final_image.paste(white_image, (0,0))
    final_image.paste(blurred_black_image, (0, 0))

    final_image.save("images\\captions\\final_output.png")

    subprocess.run(r"images\captions\final_output.png")

    colorprint('magenta', f'\tcaption {file_name} made ')


if __name__ == '__main__':

    make_caption('this is the caption', None, 'tester')