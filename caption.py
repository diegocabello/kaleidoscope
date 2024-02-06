import os

from PIL import Image, ImageDraw, ImageFont

from bigstringer import bigstringer

"""this is the colorprint"""
from colorama import Fore, Back, Style
from colorama import init as color_init

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
""""""

font_path = os.path.join('resources', 'fonts', 'EBGaramond-Medium.ttf')
font_color = (255, 255, 255)
max_width = 1536
font = ImageFont.truetype(font_path, 28)


def make_caption(text, location, file_name):

    print(text)

    file_name = str(file_name) + '.png' if not str(file_name).endswith('.png') else str(file_name)
    output_path = os.path.join(location, 'images\\captions', file_name)

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
        colorprint(cyan, wrapped_line)
        text_width, text_height = font.getsize(wrapped_line)[0], font.getsize(wrapped_line)[1]
        width_index = (max_width - text_width) // 2
        sub_image_height = text_height + buffer
        ImageDraw.Draw(final_image).text((width_index, height_index), wrapped_line, fill=font_color, font=font)
        height_index = height_index + sub_image_height

    final_image.save(output_path)
    colorprint(green, f'image {file_name} made ')

