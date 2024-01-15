import functions



# This fine tunes the gpt and produce perfect Responces

functions.response_tuner()


"""

This While loops goes on till the code is exited.
It constantly takes the commands and produce responces.

"""


forever = True

while(forever):

    functions.voice_command(6)

    command = functions.recognize_speech()

    response = functions.get_responce(command)

    functions.read_outload(response,engine="openai")



