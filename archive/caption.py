"""
the goal of this is 
define the maximum width of the textbox, make it 1344px
if it gets wider then that, it goes to a new line
"""

import os

from PIL import Image, ImageDraw, ImageFont

from bigstringer import bigstringer
import colorprint

font_path = os.path.abspath('C:\\users\\diego\\documents\\my stuff\\programming stuff\\babel\\resources\\fonts\\EBGaramond-Medium.ttf')

font_color = (255, 255, 255)
output_path = os.path.abspath('C:\\users\\diego\\documents\\my stuff\\programming stuff\\babel\\images\\captions')

max_width = 1152

def make_text_image(text, font_path, font_size, font_color, file_name):
    font = ImageFont.truetype(font_path, font_size)


    image = Image.new('RGBA', (200, 100), color = (0, 0, 0, 0))
    ImageDraw.Draw(image).text((10, 10), text, fill=font_color, font=font)
    if not file_name.endswith('.png'):
        file_name = file_name + '.png'

    image.save(os.path.join(output_path, file_name))



make_text_image(text = 'hello', font_path = font_path, font_color = font_color, font_size = 24, file_name = 'hello')

def create_centered_text_image(text, font_path, font_size, font_color, image_size, image_path):
    font = ImageFont.truetype(font_path, font_size)

    wrapped_lines = []
    words = text.split() #this is a list
    line = ''

    while font.getsize(line := line + words[0])[0] < max_width:
        words.pop(0)

    while words:
        line = ''
        while words and font.getsize(line + words[0])[0] <= max_width:
            line += words.pop(0) + ' '
        wrapped_lines.append(line.strip())
   
    dummy_draw = ImageDraw.Draw(Image.new('RGB', (1, 1))) # Calculate image height based on wrapped text
    text_height = sum([dummy_draw.textsize(line, font=font)[1] for line in wrapped_lines])
    image = Image.new('RGB', (max(image_size[0], 1152), text_height + 20), (255, 255, 255))     # Create the actual image
    draw = ImageDraw.Draw(image)
    # Draw each line of text
    y = 10  # Starting y-coordinate
    for line in wrapped_text:
        text_width, line_height = draw.textsize(line, font=font)
        x = (image.width - text_width) // 2
        draw.text((x, y), line, fill=font_color, font=font)
        y += line_height

    image.save(image_path)

def create_font_three(text, font_path, font_size, font_color, image_size, image_path):
    font = ImageFont.truetype(font_path, font_size)

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
            line = word
        if word == words[-1]:
            list_of_wrapped_lines.append(line)

    buffer = 4 # must be divisible by 2
    image_height = (font.getsize('h')[1] + buffer) * len(list_of_wrapped_lines)
    final_image = Image.new('RGBA', (max_width, image_height), color = (0, 0, 0, 0))

    list_of_line_images = []
    for wrapped_line in list_of_wrapped_lines:
        text_width, text_height = font.getsize(wrapped_line)[0], font.getsize(wrapped_line)[1]
        sub_image = Image.new('RGBA', (text_width, (text_height + buffer)), color = (0, 0, 0, 0))
        ImageDraw.Draw(sub_image).text((0, ((buffer // 2) - 1)), text, fill=font_color, font=font)
        list_of_line_images.append(sub_image)

    height_coord = 0
    for line_image in list_of_line_images:
        ImageDraw.Draw(final_image).draw(line_image, (0, height_coord))
        height_coord = height_coord + line_image.getsize[1]

    if not file_name.endswith('.png'):
        file_name = file_name + '.png'

    image.save(os.path.join(output_path, file_name))
    

    


def main():
    file_path = r'c:\users\diego\documents\my stuff\programming stuff\babel\texts\text.txt'
    list_of_lines = bigstringer(file_path).split('\r\n')



if __name__ == '__main__':
    main()




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
