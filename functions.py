import subprocess
import os
from time import sleep


# Creating a directory to store the intermediate files

cache_path = "./cache"

if not os.path.exists(cache_path):
    os.makedirs(cache_path)

"""
This Function Checks for all the dependencies and installs them if they are missing.
This might be the redundant way to do it but i guess it works pretty well.
"""

def install_depency():
    
    try: 
        from openai import OpenAI
    except ImportError:
        print("External Dependency not found Installing It......")

        subprocess.run(["pip","install","openai"])
        print("Installed Successfully\n\n\n\n\n")
        

    try:
        from playsound import playsound
    except ImportError:
        print("External Dependency not found Installing It......")

        subprocess.run(["pip","install","playsound"])
        print("Installed Successfully\n\n\n\n\n")

    try:
        import sounddevice as sound
        subprocess.run(["sudo","apt","install","libportaudio2"])

    except ImportError:

        print("External Dependency not found Installing It...........")
        subprocess.run(["pip","install","sounddevice"])

        print("Installed Successfully\n\n\n\n\n")
        
    try:
        import wave
    except ImportError:

        print("External Dependency not found Installing It..........")
        subprocess.run(["pip","install","wave"])

        print("Installed Successfully\n\n\n\n\n")


    try:
        import numpy
    except ImportError:
        print("External Dependency not found Installing It..........")
        subprocess.run(["pip","install","numpy  "])

        print("Installed Successfully\n\n\n\n\n")

    try: 
        import gtts
    except ImportError:
        print("External Dependency not found Installing It......")

        subprocess.run(["pip","install","gtts"])
        print("Installed Successfully\n\n\n\n\n")





# They are fall safe. even if the import fails
# This will import them anyways!

install_depency()

from openai import OpenAI
from playsound import playsound
import sounddevice as sound
import wave
import gtts




"""

Setting Up the open ai credentials to use it in the code further
This Includes Open ai API keys, You can get your API key from the OpenAI website - 
https://platform.openai.com/api-keys

first It creates the openai_client Instance from the OpenAI() method
which is used to get the openai API functions

"""

# OpenAI Documentation - https://platform.openai.com/docs/overview

Open_api_key = input("Paste Your OpenAi Key!")

open_client = OpenAI(api_key=Open_api_key)

gpt_model = "gpt-3.5-turbo"


"""

This function takes in the voice command using 
the sounddevice module(numpy is essentail for this module)

Param - input_time: It takes in a integer data to limit the voice input time.
Return - It returns none. But it produces a input_audio.wav file in the working Directory.

"""

# sounddevice Module Documentation - https://python-sounddevice.readthedocs.io/en/0.4.6/

# wave Module Documentation - https://docs.python.org/3/library/wave.html


def voice_command(input_time):

    print("Speak the command.....")

    playsound("./assets/input.mp3")

    Sample_rate = 8000
    input_channel = 1

    recording_chunk = sound.rec(Sample_rate*input_time,
              samplerate=Sample_rate,
              channels=input_channel,
              dtype="int16")
    
    sound.wait()
    
    with wave.open("./cache/input_audio.wav","wb") as wave_file:
        
        wave_file.setframerate(Sample_rate)
        wave_file.setnchannels(input_channel)
        wave_file.setsampwidth(2)
        wave_file.writeframes(recording_chunk)


    wave_file.close()   
    

"""
This function takes the audio file generated above and converts it into plain 
text to produce the command.

Param : none
Return : Returns the string text of the audio given as the input.

"""

# Open AI example function - https://platform.openai.com/docs/api-reference/audio/createSpeech

def recognize_speech():
    
    print("Transcribing the command!!!")

    audio_file = open("./cache/input_audio.wav","rb")

    transcription = open_client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="text"
    )

    return transcription



"""

This function fine tunes the chatgpt to be the assitant you want it to be..
You can add custom functions and limit the replies

This function should be call before the responses gathered!

Param : none
Return : none

"""


def response_tuner():

    fine_tune = "For this chat you are a assistant called 'Aurora' all you have to do is to reply the inputs in under 40 words not more then that!!! reply only 'okay' if you understand, reply shortest as you can!"

    response = open_client.chat.completions.create(
        model=gpt_model,
        messages=[{"role":"user","content":fine_tune}]    
    )

    return response.choices[0].message.content


"""

This function takes the text input that was produced from the above function
after converting the audio command and send it to the openai chat API

Param : input_string the command or text you want the gpt to respond to.

Return : Returns the string text of the output generated by the chatGPT

"""

# Openai  chat refrence - https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models

def get_responce(input_string):

    print("Generating the response!!")

    playsound("./assets/input_done.mp3")

    response = open_client.chat.completions.create(

        model=gpt_model,
        messages=[{"role":"user","content":input_string}],
        temperature=0
    )

    message = response.choices[0].message.content

    return message

"""
This function takes the generated text output and reads it outload!!

Param - input_string: Takes in the text input and generates a audio output.
        engine: the engine you want to use {"openai","gtts"}

Return : none 
         yet creates a output mp3 file which then is read by the playsound module.

"""

# Playsound Documentation - https://pypi.org/project/playsound

def read_outload(input_string,engine):

    print("Reading the response!!!")

    if engine == "gtts":

        mpeg_out = gtts.gTTS(input_string)

        mpeg_out.save("./output_speech.mp3")

    if engine == "openai":

        mpeg_out_open = open_client.audio.speech.create(

            model="tts-1",
            voice='onyx',
            input=input_string,
            speed=1.0
        )

        mpeg_out_open.stream_to_file("./cache/output_speech.mp3")

    playsound("./cache/output_speech.mp3")
    
