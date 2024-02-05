import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

#from super_parser import parse_book
from formatter import format_book
from make_video import make_video
from caption import make_caption
from make_image import make_images

def main(book_name = 'pride and prejudice'):

    counter = 0
    list_of_subvideo_paths = []
    formatted = format_book(book_name)
    prompts, bits = formatted['prompts'], formatted['bits']
    location = 'D:\\babel\\'


    for counter, (bit, prompt) in enumerate(zip(bits, prompts)):
        counter = counter + 1 
        print(bit)

        make_caption(text=bit, location=location, file_name = counter)
        make_images(prompt = prompt, location=location, file_name = counter)

        make_video(location=location, count=counter)

        list_of_subvideo_paths.append(os.path.join(location, 'subvideos', str(counter) + '.mp4'))
        print(f'made subvideo {str(counter)} ')


    subvideo_clips = [VideoFileClip(path) for path in list_of_subvideo_paths]
    concatenated_clip = concatenate_videoclips(subvideo_clips)
    concatenated_clip.write_videofile("output.mp4")


if __name__ == '__main__':
    main()