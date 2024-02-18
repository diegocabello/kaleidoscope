import os
from datetime import datetime 
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips

#from super_parser import parse_book
from formatter import format_book
from make_video import make_video
from caption import make_caption
from make_image import make_images
from colorprint import colorprint

def main(book_name = 'dracula'):

    list_of_subvideo_paths = []
    formatted = format_book(book_name)
    prompts, bits = formatted['prompts'], formatted['bits']
    location = 'D:\\babel\\'

    directories = ['images', 'images\\backgrounds', 'images\\captions', 'subvideos', 'audio']
    location = os.path.join(location, book_name)

    if not os.path.isdir(location): 
        os.mkdir(location)
        for directory in directories:
            os.mkdir(os.path.join(location, directory))       

    for counter, (bit, prompt) in enumerate(zip(bits, prompts)):

        make_caption(text=bit, location=location, file_name = counter)

        make_images(prompt = prompt, location=location, file_name = counter)

        make_video(location=location, file_name=counter)

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