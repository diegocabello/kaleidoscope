import subprocess
from pydub import AudioSegment
import ffmpeg
import os

class video_inputs:
    def __init__(self, image, blurred_image, audio, audio_duration):
        self.image = image
        self.blurred_image = blurred_image
        self.audio = audio
        self.audio_duration = audio_duration
  
    
def sotr(number_frames=10):
    dicto = {}
    for x in range(1, number_frames + 1):
        audio_path = f"D:\\babel2\\audio\\{x}.mp3"
        dicto[x] = video_inputs(
            image = f"D:\\babel2\\images\\cropped\\{x}.png", 
            blurred_image = f"D:\\babel2\\images\\zoomed_and_blurred\\{x}.png", 
            audio = audio_path, 
            audio_duration = (len(AudioSegment.from_file(audio_path)) / 1000)
        )
    return dicto


def stitch(foldername=''):
    path = os.path.abspath(foldername)
    subvidtxt = os.path.join(path, 'listofsubvideos.txt')
    #clear
    with open(subvidtxt, 'w') as file:          # the subvideos index
        file.write('')
    for filename in os.listdir('subvideos'):                # the subvideos folder
        file_path = os.path.join('subvideos', filename)
        if os.path.isfile(file_path):                       # Check if it's a file and not a directory
            os.remove(file_path)
    if os.path.isfile('output.mp4'):                        # the output video 
        os.remove('output.mp4')
                                    

    # Create a bunch of subvideos
    for x in sotr():
        subvideo_command = f'ffmpeg -loglevel warning -loop 1 -framerate 10 -i {x.image} -i {x.audio} -c:v libx264 -t {x.audio_duration}  \
            -pix_fmt yuv420p {path}\\subvideos\\{x}.mp4'        

        subprocess.run(subvideo_command, shell=True)
        with open(subvidtxt, 'a') as file:
            file.write(f"file '{path}\\subvideos\\{x}.mp4'\n")

    # concatenate them into output video
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-loglevel', 'warning', '-i', subvidtxt,  
                    '-c', 'copy', f'{path}\\output.mp4'])


# Add audio to the slideshow
# subprocess.run(["ffmpeg", "-i", "slideshow.mp4", "-i", "combined_audio.mp3", 
#                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "final_video.mp4"])


#super important
#lister = [f"{x}.mp3" for x in range(1, 10)]
#print(', '.join(f"{x}" for x in range(1, 11)))

#methods are functions defined within a class
#object is an instance of a class 
#dir()
# use try and except to check if something exists
# its called list comprehensions
#[x + y for x in list1 for y in list2]
#what you are looking for is the "zip" function which takes two lists and returns an list of ordered tuples pairs 
# [:str(number).find('.')+2]
# print([x+1 for x in range(len(image_files))])
    # put it in a list 

# this too 
# print(*[x for x in text['sentences'][0:10]], sep='\n')
# dir() thats what its called dir()
# print(*(x for x in [1, 2]))
#  print(*(x for x in [1, 2]), sep='\n')
# you can list() on a generator object 