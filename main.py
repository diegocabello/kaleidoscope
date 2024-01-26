import openai
from openai import OpenAI
import os

from imagetest import create_image, crop
from soundtest import create_audio
from bigstringer import bigstringer
from stitch import stitch
from openaitest import chatgpt, logline
from text_parser import sentencer  

client = OpenAI()

sentences = sentencer(category='file', input='pride and prejudice chapter 2.txt')

inputer = """
\n the style should be photorealistic and consistent with the previous images. this is from the novel pride and prejudice, taking place in the 1800s in upscale victorian england. all the costumes and settings should be made to match the time periods. 
"""
inputer2='''the style should be photorealistic and consistent with the previous images. this is from the memoars of casanova, taking place in the 1700s europe, primarily in italy. all the costumes and settings should be made to match the time periods. 
'''

for counter, value in enumerate(sentences[0:10]):
    counter = counter + 1
    value = str(value).strip('\n')
    prompter = value + inputer2
    print(value)
    print('\n')
    try:
        create_image(prompt= prompter,
                     filelocation = 'D:\\babel2\\images',
                     filename=str(counter))
        crop(filelocation='D:\\babel2\\images')
        create_audio(prompt=value, filelocation='D:\\babel2\\audio', filename=str(counter))
    except openai.BadRequestError:
        pass


stitch(foldername='D:\\babel2\\video')
                                                                                    