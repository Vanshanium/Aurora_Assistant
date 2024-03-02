

import functions

# This fine tunes the gpt and produce perfect Responces


print("The modules are loading please wait.....")
functions.response_tuner()


"""

This While loops goes on till the code is exited.
It constantly takes the commands and produce responces.

terminate the program with ctrl+c in the terminal!

"""


forever = True

while(forever):

    functions.voice_command(4)

    command = functions.recognize_speech()

    response = functions.get_responce(command)

    functions.read_outload(response,engine="openai")
