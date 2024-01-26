import moviepy.editor as mp
import math
from PIL import Image
import numpy
import sympy as sp


size = (1920, 1080)

def zoom_in_effect(clip, start_percentage=75, end_percentage = 90):

    def zoom_ratio(frame_number = 1,
                    halfway_point = 5, fps = 25):
        diff_ratio = (end_percentage / start_percentage) - 1
        halfway_point = halfway_point * fps
        #
        x = sp.symbols('x')
        eq = sp.Eq(((-1/x) + diff_ratio), 0)
        zero = sp.solve(eq, x)[0]
        #
        multiplier = (-1/(frame_number + zero)) + diff_ratio
        multiplier = multiplier + 1
        #
        return multiplier

    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        #base_size = img.size
        base_size = [x * (start_percentage/100) for x in img.size]

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)


images = [
    'https://www.colorado.edu/cumuseum/sites/default/files/styles/widescreen/public/slider/coachwhip2_1.jpg',
    'https://www.colorado.edu/cumuseum/sites/default/files/styles/widescreen/public/slider/green2_1.jpg',
    'https://www.colorado.edu/cumuseum/sites/default/files/styles/widescreen/public/slider/westterrgarter_1.jpg',
    'https://www.colorado.edu/cumuseum/sites/default/files/styles/widescreen/public/slider/prairierattle4.jpg'
]

slides = []
for n, url in enumerate(images):
    slides.append(
        mp.ImageClip(url).set_fps(25).set_duration(5).resize(height=1080)
    )

    slides[n] = zoom_in_effect(slides[n], 0.04)



video = mp.concatenate_videoclips(slides)
video.write_videofile('zoomin.mp4')