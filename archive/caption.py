import os

from PIL import Image, ImageDraw, ImageFont

from bigstringer import bigstringer
from colorprint import colorprint

font_path = os.path.abspath('C:\\users\\diego\\documents\\my stuff\\programming stuff\\babel\\resources\\fonts\\EBGaramond-Medium.ttf')
font_color = (255, 255, 255)
output_path = os.path.abspath('C:\\users\\diego\\documents\\my stuff\\programming stuff\\babel\\images\\captions')
max_width = 1536
font = ImageFont.truetype(font_path, 28)

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

def unpack(inputer):
    print(*(x for x in inputer), sep='\n')
""""""


def create_caption_image(text, file_name):

    list_of_wrapped_lines = []
    words = text.split() #this is a list of words
    line = ''
    file_name = str(file_name)

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


    if not file_name.endswith('.png'):
        file_name = file_name + '.png'

    final_image.save(os.path.join(output_path, file_name))
    colorprint(green, f'image {file_name} made ')
    



if __name__ == '__main__':
    file_path = r'c:\users\diego\documents\my stuff\programming stuff\babel\texts\test.txt'
    list_of_lines = bigstringer(file_path).split('\r\n')
    for count, line in enumerate(list_of_lines):
        create_caption_image(line, (count+1))


"""

while font.getsize(line := line + words2[0] + ' ')[0] < max_width:
    words2.pop(0)

#this works but is not compact at all
line = ''
wrapped_lines = []
for word in words: 
    line_clone = line + word + ' '
    if font.getsize(line_clone)[0] < max_width:
        line = line + word + ' '
    else:
        wrapped_lines.append(line)
        line = word
    if word == words[-1]:
        wrapped_lines.append(line)



wrapped_lines = []
wrapped_lines.extend(line := line + word + ' ' for word in words if font.getsize(line) < max_width else wrapped_lines.append(line), line = '')
wrapped_lines.extend((line := line + word + ' ') if font.getsize(line + word)[0] < max_width else (wrapped_lines.append(line), line := '') for word in words)


line = ' '.join(word for word in words if font.getsize(line)[0] < max_width)
"""
