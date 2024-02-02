import os

from super_parser import parse_book
from formatter import format_prompts
from make_video import make_video
from caption import make_caption
from make_image import make_images

book_name = 'alice in wonderland'

prompts, bits = format_prompts['prompts'], format_prompts['bits']

location = None

def main():

    global location 

    for counter, (bit, prompt) in enumerate(zip(bits, prompts)):
        counter = counter + 1 

        make_caption(text=bit, location=location, file_name = counter)
        make_images(prompt = prompts[counter - 1], location=location, file_name = counter)
        make_video(location=location, count=counter)