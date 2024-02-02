import openai
import os

def create_audio(prompt="", filelocation = "", filename=""):

    speech_file_path = os.path.join(filelocation, f'{filename}.mp3')

    response = openai.audio.speech.create(
    model="tts-1",
    voice="fable",
    input=prompt
    )

    response.stream_to_file(speech_file_path)

    print(f'generated audio {filename} ')

