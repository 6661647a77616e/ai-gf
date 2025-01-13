from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from TTS.api import TTS
import requests
import json
import pygame
import time

# Function to play audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Function to fetch AI response
def fetch_ai_response(user_input):
    url = "http://192.168.56.1:8001/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
            {"role": "user", "content": user_input},
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    return response_data['choices'][0]['message']['content']

# 3D Application Class
class Character3DApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the 3D character model and animations
        self.character = Actor("models/character.egg",
                               {"talk": "models/character_walk.egg"})
        self.character.reparent_to(self.render)
        self.character.set_scale(0.5)
        self.character.set_pos(0, 10, 0)

    def speak(self, text_reply):
        # Use TTS to generate speech
        tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to("cpu")
        tts.tts_to_file(text=text_reply, file_path="output.wav")

        # Play the audio
        play_audio("output.wav")

        # Animate character while speaking
        self.character.loop("talk")

# Main Script
if __name__ == "__main__":
    user_input = input("> ")
    ai_reply = fetch_ai_response(user_input)

    app = Character3DApp()
    app.speak(ai_reply)

    app.run()
