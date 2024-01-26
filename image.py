import base64
import os
from openai import OpenAI
import json
import subprocess
from openaitest import chatgpt

#client = OpenAI()


def create_image(prompt='', filelocation='', filename=''):

    try:
        if client:
            pass
    except NameError:
        client = OpenAI()

    #↓ calls openai api
    response = client.images.generate(model="dall-e-3", prompt=prompt, size="1792x1024", quality="standard", n=1, response_format = 'b64_json')

    #↓ parses b64 data
    image_bytes = base64.b64decode(json.loads(response.model_dump_json(exclude=['url', 'revised_prompt']))["data"][0]["b64_json"])  

    #↓ Write to a PNG file
    filename = os.path.join(f'{os.path.abspath(filelocation)}', f'{filename}.png')
    with open(f'{filename}.png', 'wb') as file:
        file.write(image_bytes)

    print(f'generated image {filename}')





def crop(filelocation=''):
    path = os.path.abspath(filelocation)
    for image in os.listdir(path):
        image_path = os.path.join(path, image)
        if os.path.isfile(image_path):
            cropped_image_path = os.path.join(path, 'cropped', image)
            cmd = f'ffmpeg -i {image_path} -vf "crop=1792:1008:0:8" {cropped_image_path}'
            subprocess.run(cmd, shell=True)

def blur(filelocation='D:\\babel2\\images'):
    path = os.path.abspath(filelocation)
    for image in os.listdir(path):
        cropped_image_path = os.path.join(path, 'cropped', image)
        blurred_image_path = os.path.join(path, 'zoomed_and_blurred', image)
        cmd = f'ffmpeg -i {cropped_image_path} -vf "zoompan=z=\'zoom+0.3\':d=1:s=1920x1080, boxblur=15" -frames:v 1  {blurred_image_path}'
        cmd = f'ffmpeg -i {cropped_image_path} -vf "zoompan=z=\'min(zoom+0.3,2.0)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s=1920x1080, \
        boxblur=15" -frames:v 1 {blurred_image_path}'
        subprocess.run(cmd, shell=True)
        

if __name__ == "__main__":
    prompt=input('what would you like to generate? ')
    filename=input('what would you like to call your file? ')

    try:
        if client:
            pass
    except NameError:
        client = OpenAI()

    #↓ calls openai api
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    quality="standard",
    n=1,
    response_format = 'b64_json'
    )

    #↓ parses b64 data
    stringer = response.model_dump_json(exclude=['url', 'revised_prompt'])
    stringer2 = json.loads(stringer)["data"][0]["b64_json"]
    image_bytes = base64.b64decode(stringer2) 

    image_file_path = os.path.join('images', f'{filename}.png')

    # Write to a PNG file
    with open(image_file_path, 'wb') as file:
        file.write(image_bytes)

    print(f'generated image {filename}')
