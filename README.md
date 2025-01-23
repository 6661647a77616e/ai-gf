
---

# Character Interaction Application

This application allows you to interact with an AI-powered character that responds to your questions in rhymes. The character's visual representation changes between a static image (`silent.png`) and an animated GIF (`talk.gif`) while speaking. The application uses the `TTS` library for text-to-speech synthesis and `pygame` for rendering the visuals.

---



## Setup Instructions

### 1. Create a Virtual Environment

To create a virtual environment using `uv`, run the following command:

```bash
uv venv
```

This will create a virtual environment in the `.venv` directory.

---

### 2. Activate the Virtual Environment

Activate the virtual environment using the appropriate command for your operating system:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  source .venv/bin/activate
  ```

---

### 3. Install Dependencies

Install the required dependencies using `uv`:

```bash
uv pip install -r requirements.txt
```

---

### 4. Download the TTS Model

The application uses the `tts_models/en/jenny/jenny` model for text-to-speech synthesis. Download the model using the following command:

```bash
tts --model_name tts_models/en/jenny/jenny
```

You can verify that the model has been downloaded by listing all available models:

```bash
tts --list_models
```

Look for `tts_models/en/jenny/jenny` in the output.

---

## Running the Application

1. Ensure the virtual environment is activated.
2. Run the application using Python:

   ```bash
   python app/app.py
   ```

3. The application will start by displaying the `silent.png` image. Type your question in the terminal and press Enter.
4. The AI will generate a response, and the application will display the `talk.gif` animation while playing the synthesized speech.
5. After the speech finishes, the application will return to displaying `silent.png` and wait for the next question.

To exit the application, type `exit` or `quit` in the terminal.

## Notes

- Ensure `silent.png` and `talk.gif` are in the same directory as the script or provide the correct paths.
- The application uses `pygame` for rendering visuals. If you encounter issues, ensure `pygame` is installed correctly.
- The `clock.tick(10)` in the code controls the speed of the GIF animation. Adjust this value to match the speed of your GIF.

---

## Troubleshooting

- **Model Not Downloading**: Ensure you have a stable internet connection. If the model fails to download, try running the `tts --model_name tts_models/en/jenny/jenny` command again.
- **Pygame Issues**: If `pygame` does not work correctly, reinstall it using `uv pip install pygame`.
- **GIF Animation Issues**: Ensure `talk.gif` is a valid animated GIF. You can test it using an image viewer.

---

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---

Enjoy interacting with your AI-powered character! 😊
