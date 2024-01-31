import os

from super_parser import parse_book
from formatter import format_prompts
from make_video import make_sub_video

book_name = 'alice in wonderland'

def text_to_speech():
    pass
def generate_image():
    pass

list_of_prompts = format_prompts(book_name)
list_of_bits = []
list_of_sub_video_paths = []
list_of_audio_paths = []

for bit_counter, bit in enumerate(list_of_bits):
    text_to_speech(bit, bit_counter)
    list_of_audio_paths.append(os.path.abspath(f'audio\\{str(bit_counter + 1).mp3}'))
for prompt_counter, prompt in enumerate(list_of_prompts):
    generate_image(prompt, prompt_counter)
    list_of_sub_video_paths.append(os.path.abspath(f'subvideos\\{(str(prompt_counter + 1).mp4)}'))

for counter, (audio, video) in enumerate(zip(list_of_audio_paths, list_of_sub_video_paths)):
    make_sub_video((counter + 1), audio, video)
