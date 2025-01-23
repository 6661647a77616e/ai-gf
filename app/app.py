from TTS.api import TTS
import requests
import json
import pygame
import time
import sys
import os
from PIL import Image, ImageSequence  # For handling GIF frames

# Initialize pygame
pygame.init()

# Load the silent image to determine the window size
silent_image = pygame.image.load("silent.png")
window_width, window_height = silent_image.get_size()

# Set up the display to match the image size
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Character Interaction")

# Load silent image
image_silent = silent_image

# Load the talking GIF and extract its frames
def load_gif_frames(gif_path, target_size):
    try:
        gif = Image.open(gif_path)
        frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            frame = frame.resize(target_size)
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_frame)
        return frames
    except Exception as e:
        print("Error loading GIF:", e)
        return []

# Load talking GIF frames
talking_frames = load_gif_frames("talk.gif", (window_width, window_height))
current_frame = 0

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Function to display text input box
def draw_text_input_box(text):
    input_box = pygame.Rect(50, window_height - 80, window_width - 100, 50)
    pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    txt_surface = FONT.render(text, True, BLACK)
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
    pygame.display.flip()

# Function to play audio and safely delete the file
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        display_talking()  # Display animation while audio is playing
        pygame.time.delay(100)  # Delay for smooth animation

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    time.sleep(0.5)  # Ensure file handle is released before deletion
    if os.path.exists(file_path):
        os.remove(file_path)

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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error fetching AI response: {str(e)}"

# Function to display the talking animation
def display_talking():
    global current_frame
    if talking_frames:
        screen.blit(talking_frames[current_frame], (0, 0))
        pygame.display.flip()
        current_frame = (current_frame + 1) % len(talking_frames)
    else:
        display_silent()

# Function to display the silent image
def display_silent():
    screen.blit(image_silent, (0, 0))
    pygame.display.flip()

# Main Script
if __name__ == "__main__":
    # Initialize TTS
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to("cpu")

    running = True
    clock = pygame.time.Clock()
    user_text = ""  # User input text
    input_active = True  # Track input status

    while running:
        # Display the silent image initially
        display_silent()
        draw_text_input_box(user_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.lower() in ["exit", "quit"]:
                        running = False
                        break  # Exit the loop if the user types "exit" or "quit"

                    # Fetch AI response
                    ai_reply = fetch_ai_response(user_text)
                    print("AI:", ai_reply)

                    # Clean the AI response text
                    ai_reply = ai_reply.replace("\n", " ").strip()

                    # Save audio to current directory as output.wav
                    audio_file_path = "output.wav"
                    try:
                        tts.tts_to_file(text=ai_reply, file_path=audio_file_path)

                        # Play the audio and display the talking GIF animation
                        play_audio(audio_file_path)

                        # After audio finishes, display the silent image again
                        display_silent()

                    except Exception as e:
                        print("Error generating audio:", e)

                    user_text = ""  # Clear input after processing

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]  # Remove last character
                else:
                    user_text += event.unicode  # Add character to input text

        clock.tick(30)  # Limit frame rate to avoid high CPU usage

    # Clean up and exit
    pygame.quit()
    sys.exit()
