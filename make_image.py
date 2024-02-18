import os 
import subprocess
from PIL import Image 

from midjourney_api import MidjourneyApi
from colorprint import colorprint

size = (1920, 1080)
padding = 80
total_size = tuple(x + (padding * 2) for x in size)

authorization = 'NTcwMjgwMTcxMzI0ODMzODEz.G2CQOZ.hYckkjT5gRqa381BPi1hzTOucxeZtdcEdqmVKw' # this is the one that needs to be updated each time 
application_id = '936929561302675456'
guild_id = '884622163146059826'
channel_id = '1201996275160191027'
version = '1166847114203123795'
id = '938956540159881230'

def make_images(prompt='', location=None, file_name=None):

    file_name = str(file_name)

    api_instance = MidjourneyApi(prompt=prompt, location=location, file_name=file_name, application_id=application_id, guild_id=guild_id, channel_id=channel_id, version=version, id=id, authorization=authorization)
    api_instance.send_message()
    api_instance.get_message()
    api_instance.choose_images()
    api_instance.download_image()

    colorprint('magenta', f'\tmade image {file_name} ')

    if location: 
        background_path = os.path.join(location, "images\\backgrounds", file_name + '.png')
        image_path = os.path.join(location, "images", file_name + '.png')
    else: 
        background_path = os.path.join("images\\backgrounds", file_name + '.png')
        image_path = os.path.join("images", file_name + '.png')

    overlay_path = os.path.join('resources', 'overlay.png')

    # ZOOM IN AND BLUR BACKGROUND 
    #cmd = f'ffmpeg -i {image_path} -vf "zoompan=z=\'zoom+0.3\':d=1:s=1920x1080, boxblur=15" -frames:v 1  -loglevel warning {background_path}'
    cmd = f'ffmpeg -i "{image_path}" -vf "zoompan=z=\'min(zoom+0.3,2.0)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s=1920x1080, \
    boxblur=15" -frames:v 1 -loglevel error "{background_path}"'
    subprocess.run(cmd, shell=True)

    # DARKEN BACKGROUND 
    overlay_obj = Image.open(overlay_path)
    background_obj = Image.open(background_path)
    background_obj.paste(overlay_obj, (0, 0),  overlay_obj.convert("RGBA"))    #darken background image
    background_obj.save(background_path)

if __name__ == '__main__':
    pass