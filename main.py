import os
from datetime import datetime 
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips

#from super_parser import parse_book
from formatter import format_book
from make_video import make_video
from make_caption import make_caption
from make_image import make_images
from make_audio import make_audio
from colorprint import colorprint

def main(book_name = 'dracula'):

    location = 'D:\\babel\\'
    list_of_subvideo_paths = []
    formatted = format_book(book_name)
    prompts, bits = formatted['prompts'], formatted['bits']

    directories = ['images', 'images\\backgrounds', 'images\\captions', 'images\\captions\\components', 'subvideos', 'audio']
    location = os.path.join(location, book_name)

    if not os.path.isdir(location): 
        os.mkdir(location)
    for directory in directories:
        to_make_dir = os.path.join(location, directory)
        if not os.path.isdir(to_make_dir):
            os.mkdir(to_make_dir)       

    def constructor(counter, bit, prompt):
        sub_counter = 0
        audio_paths = []

        caption_return_dictionary = make_caption(text=bit, location=location, file_name = counter) # determines how much text fits into each caption space, cuts it up, makes caption, returns the cut up text parts and caption locations
        text_segments, caption_paths = caption_return_dictionary["text"], caption_return_dictionary["locations"]

        for audio in text_segments:
            sub_counter += 1
            audio_path = make_audio(audio, location, counter, sub_counter) # returns the audio path for however many subaudios are in there
            audio_paths.append(audio_path)

        #make_images(prompt = prompt, location = location, file_name = counter)
        make_video(location=location, file_name=counter, audio_paths = audio_paths, caption_paths = caption_paths)

    for counter, (bit, prompt) in enumerate(zip(bits, prompts)): 
        counter += 1
        constructor(counter, bit, prompt)

        list_of_subvideo_paths.append(os.path.join(location, 'subvideos', str(counter) + '.mp4'))
        colorprint('red', f'made subvideo {str(counter)} ')

    subvideo_clips = [VideoFileClip(path) for path in list_of_subvideo_paths]
    concatenated_clip = concatenate_videoclips(subvideo_clips)

    run_log_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = os.path.join("outputs", f"{book_name} {run_log_time}.mp4")
    concatenated_clip.write_videofile(file_name)

    subprocess.run(file_name, shell=True)


if __name__ == '__main__':
    main(book_name = 'alice in wonderland')