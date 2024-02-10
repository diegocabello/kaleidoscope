import moviepy.editor as mp
import math
from PIL import Image
import numpy
import subprocess

size = (1920, 1080)
#image_path = r'd:\babel\dracula\images\backgrounds\2.png'
image_path = r"C:\Users\diego\Downloads\wp4939880-fantasy-vintage-wallpapers.png"


def make_zoomin_background(input_image, duration):
    frame_counter = 0

    def zoom_in_effect(clip, zoom_ratio=0.018):

        def effect(get_frame, t):
            nonlocal frame_counter 
            frame_counter += 1 
            print(frame_counter)

            img = Image.fromarray(get_frame(t))
            base_size = img.size

            new_size = [
                math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
                math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
            ]

            new_size[0] = new_size[0] + (new_size[0] % 2)
            new_size[1] = new_size[1] + (new_size[1] % 2)

            img = img.resize(new_size, Image.LANCZOS)

            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2)

            img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result

        return clip.fl(effect)

    return zoom_in_effect(mp.ImageClip(input_image).set_fps(24).set_duration(duration).resize(size), 0.04)

if __name__ == '__main__':

    make_zoomin_background(image_path, 5).write_videofile('zoomin3.mp4')
    subprocess.run(r'zoomin3.mp4', shell=True)
