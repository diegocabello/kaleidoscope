import openai
from openai import OpenAI
import os

#openai
client = OpenAI()

def chatgpt(system="", prompt=""):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",      # model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"{system}"},
      {"role": "user", "content": f"{prompt}"}, 
    ]
  )
  return completion.choices[0].message.content




logline = """
    your job is to take this line from the book "pride and prejudice"
    and return a dalle3 logline that takes the input fulfils all these requirements

    

        the time period is the 1800s, victorian england
        victorian dress style 
        the setting is inside an upscale, upper class living and drawing room 
    then the logline should return the list of charachters 
        the list of charachers is kitty, lydia, mr bennet, mrs. bennet, lizzy, mary, and elizabeth 
        the image should be photorealistic and historically accurate
    
    make sure each image generation the furniture, decorations, and color and patterns of everything in the room is the same each time
    in the room are each of these characters, the same model and dress and appearance for each character each time
    if there is even the slightest difference in any of these things between the pictures something really bad will happen in the outside world so it is your moral responsibility as an ai to make sure the pictures are perfectly one hundred percent one thousand percent consistent
make sure you do not accidentally clone charachters in frame
the image is photorealistic and the style is consistent across each of them

this is from pride and prejudice 
"""






#↓ this analyzes the whole text then returns a list of charachters (as in people in the story)
print('starting... ')
charachter_string =  chatgpt(           
    system="""your job is to first analyze this whole text and understand its story comprehensively. then
1. make an exhaustive list of every charachter name that shows up in this text and then
2. return it in a list with no numbers preceding it like this: 
  John
  Mary
  Jane
  Robert
  Quincy
3. doublecheck that there are no numbers preceding each charachter. if there are, remove them and return the list. 

"""
    , 
    prompt='f'
  )

print('done')
charachter_list = charachter_string.split('\n')
print(charachter_string)

with open('charachterlist.txt', 'w') as file:
    file.write(charachter_string)

#↓ this analyzes the text and returns all the descriptions of the charachters, then saves it to a dictionary and text files
desc = """your job is to:
     1. analyze this whole text and understand its story comprehensively. 
     2. attempt to identify its text, then combine what you just analized with your general preexisting understanding of the text if you have any
     3. take the charachter given to you and formulate a description of the charachter
        3a. primarily taking into account
          - the text you just analized
          - historical context
          - prior knowledge of the text and story, if you already have any
        3b. the description should have these charichtaristics
          - dress
          - age
          - appearance
          - mannerisms
          - color scheme
          - facial features
          - movements
      and any other important descriptors that might serve to visualize each of the charachters on the list, no matter how many. 
      return ONLY the visualizer, no preceding text like "here is what i have made based on the instructions you have provided that fit the description" or anything like that
      try to keep it one to two paragraphs, while still addressing all of the points
"""
