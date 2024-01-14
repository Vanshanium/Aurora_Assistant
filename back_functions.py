import subprocess
from time import sleep

try: 
    from openai import OpenAI
except ImportError:
    print("External Dependency not found Installing It......")

    subprocess.run(["pip","install","openai"])
    print("Installed Successfully\n\n\n\n\n")
    from openai import OpenAI

try:
    from playsound import playsound
except ImportError:
    print("External Dependency not found Installing It......")

    subprocess.run(["pip","install","playsound"])
    print("Installed Successfully\n\n\n\n\n")
    from playsound import playsound

try:
    import sounddevice as sound

except ImportError:

    print("External Dependency not found Installing It...........")
    subprocess.run(["pip","install","sounddevice"])

    print("Installed Successfully\n\n\n\n\n")
    
    import sounddevice as sound

try:
    import wave
except ImportError:

    print("External Dependency not found Installing It..........")
    subprocess.run(["pip","install","wave"])

    print("Installed Successfully\n\n\n\n\n")

    import wave

try:
    import numpy
except ImportError:
    print("External Dependency not found Installing It..........")
    subprocess.run(["pip","install","numpy  "])

    print("Installed Successfully\n\n\n\n\n")


Open_api_key = "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"

open_client = OpenAI(api_key=Open_api_key)


def voice_command(input_time):

    print("Speak the command.....")

    Sample_rate = 8000
    input_channel = 1

    recording_chunk = sound.rec(Sample_rate*input_time,
              samplerate=Sample_rate,
              channels=input_channel,
              dtype="int16")
    
    sound.wait()
    
    with wave.open("./input_audio.wav","wb") as wave_file:
        
        wave_file.setframerate(Sample_rate)
        wave_file.setnchannels(input_channel)
        wave_file.setsampwidth(2)
        wave_file.writeframes(recording_chunk)


    wave_file.close()
    
    print("Command taken!!!")

def recognize_speech():

    audio_file = open("./input_audio.wav","rb")

    transcription = open_client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="text"
    )

    return transcription


def get_responce():
    
    print() 

def read_output(input_string):
    
    print()