import os

from google.cloud import texttospeech
from colorprint import colorprint

def make_audio(text, location, counter, subcounter): 
    
    if location and subcounter:
        output_path = os.path.join(location, 'audio', f'{str(counter)}_{str(subcounter)}.wav')
    elif subcounter:
        output_path = os.path.join('audio', f'{str(counter)}_{str(subcounter)}.wav')
    else:
        output_path = os.path.join('audio', f'{counter}.wav')

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-AU", name="en-AU-Wavenet-D")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output_path, "wb") as out:
        out.write(response.audio_content)

    colorprint("magenta", f"\taudio {counter}-{subcounter} made")

    return output_path