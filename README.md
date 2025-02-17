# AI-Powered Song Generator

## Overview
This project generates a complete song based on a given book summary. It uses AI to:
- Detect the genre of the book summary.
- Generate lyrics in the detected genre.
- Create vocals using a Text-to-Speech (TTS) model.
- Generate background music that matches the lyrics.
- Merge vocals and background music into a final song.

## Technologies Used
- **Cohere API**: For genre detection, lyric generation, and music description.
- **TTS (Text-to-Speech)**: For generating vocals.
- **MusicGen**: For creating background music.
- **Flask**: For providing an API interface.
- **Pydub**: For audio merging and manipulation.
- **Torchaudio**: For audio processing.

## Installation
### Prerequisites
Make sure you have Python installed. Then, install the required dependencies:

```sh
pip install cohere torch torchaudio TTS audiocraft pydub flask
```

### Additional Requirements
- **Cohere API Key**: You need a Cohere API key to generate lyrics and detect genre.
- **Reference Voice**: Place a `reference_voice.wav` file in the same directory. This is required for generating vocals.
- **FFmpeg**: Ensure `ffmpeg` is installed for `pydub` to process audio files.

## Usage
### 1. Start the Flask Server
Run the following command to start the server:

```sh
python app.py
```

The server will start at `http://127.0.0.1:5000/`

### 2. Generate a Song
Make a POST request to `/generate_song` with a JSON payload:

#### Request Example:
```json
{
    "book_summary": "A thrilling adventure about a group of explorers uncovering ancient secrets."
}
```

#### Response Example:
```json
{
    "lyrics": "[Generated song lyrics]",
    "genre": "Rock",
    "download_url": "/download_song?file=final_song.mp3"
}
```

### 3. Download the Generated Song
Once the song is generated, use the `download_url` from the response to download the final song.

Example:
```
http://127.0.0.1:5000/download_song?file=final_song.mp3
```

## Notes
1. Use your **Cohere API Key** in `COHERE_API_KEY`.
2. Provide a **reference voice** file (`reference_voice.wav`) in the same directory.
3. Install the **necessary dependencies** before running the project.

---
Enjoy generating AI-powered music! 🎵
