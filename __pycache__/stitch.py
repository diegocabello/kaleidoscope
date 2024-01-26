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
                                    

    #cropped_image_files = [f"D:\\babel2\\images\\cropped\\{x}.png" for x in range(1,(10+1))]
    #cropped_zoomed_and_blurred_image_files = [f"D:\\babel2\\images\\zoomed_and_blurred\\{x}.png" for x in range(1,(10+1))]
    #audio_files = [f"D:\\babel2\\audio\\{x}.mp3" for x in range(1,(10+1))]
    #audio_durations = [(len(AudioSegment.from_file(audio)) / 1000) for audio in audio_files] # duration in seconds
    #count = [x+1 for x in range(len(cropped_image_files))]


    # Create a bunch of subvideos
    for cropped_image, czb_image, audio, duration, counter in \
        zip(cropped_image_files, cropped_zoomed_and_blurred_image_files, audio_files, audio_durations, count):
        #audio_segment = AudioSegment.from_file(audio)
        #len_audio_seconds = len(audio_segment) / 1000  # duration in seconds
        #this one does it in a list, just puts picture there for length of audio
        #subprocess.run(["ffmpeg", "-loop", "1", "-framerate", "10", "-i", str(image), "-i", str(audio), 
        #                "-c:v", "libx264", "-t", str(len_audio_seconds), 
        #                "-pix_fmt", "yuv420p", f"subvideos\\{counter}.mp4"])
        #this one puts it all into a string
        subvideo_command = f'ffmpeg -loglevel warning -loop 1 -framerate 10 -i {str(cropped_image)} -i {str(audio)} -c:v libx264 -t {str(duration)}  \
            -pix_fmt yuv420p {path}\\subvideos\\{counter}.mp4'
        #this one puts blurred image and then zooms in on second image
        #subvideo_command = f'ffmpeg -loop 1 -i {czb_image} -loop 1 -i {cropped_image} -filter_complex \
        #        "[1:v]scale=iw*0.75:ih*0.75,zoompan=z=\'min(zoom+0.002,0.95)\':d=({duration}*25):x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1920x1080[zoomed]; \
        #        [0:v][zoomed]overlay=(W-w)/2:(H-h)/2" -t {duration} -c:v libx264 {counter}.mp4'
        

        subprocess.run(subvideo_command, shell=True)
        with open(subvidtxt, 'a') as file:
            file.write(f"file '{path}\\subvideos\\{counter}.mp4'\n")

    # concatenate them into output video
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-loglevel', 'warning', '-i', 'subvidtxt.txt',  '-c', 'copy', f'{path}\\output.mp4'])


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