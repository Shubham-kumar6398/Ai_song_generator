import cohere
import torch
import torchaudio
from flask import Flask, request, jsonify, send_file
from TTS.api import TTS
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pydub import AudioSegment 
import os

# Initialize Flask app

app = Flask(__name__)

# Initialize Cohere API
COHERE_API_KEY = "API_KEY"
co = cohere.Client(COHERE_API_KEY)

# Initialize TTS Model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")  # Use GPU

# Initialize Music Generation Model
music_model = MusicGen.get_pretrained('facebook/musicgen-small')

def detect_genre(book_summary):
    genre_prompt = (
        f"Analyze the tone and theme of the following book summary and suggest an appropriate music genre: {book_summary}. "
        "Respond with only one word from the following options: Pop, Rock, Jazz, Hip-Hop, or Classical."
    )
    
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=genre_prompt,
        max_tokens=1,
        temperature=0.5
    )
    
    genre = response.generations[0].text.strip()
    if genre not in ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical"]:
        genre = "Pop"
    
    return genre

def get_audio_duration(file_path):
    waveform, sample_rate = torchaudio.load(file_path)
    return waveform.shape[1] / sample_rate

def generate_lyrics(book_summary):
    genre = detect_genre(book_summary)
    prompt = (
        f"Write a complete song based on this book summary: {book_summary}. "
        f"The song should follow the {genre} style. Ensure that all verses, chorus, "
        f"and bridge are complete and do not end mid-line. Do not include section labels. "
        "Write exactly six stanzas, ensuring smooth transitions between them."
    )
    
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.8
    )
    
    return genre, response.generations[0].text.strip()

def generate_music_prompt(lyrics):
    prompt = (
        f"Based on the following lyrics, generate a fitting music description: {lyrics}. "
        "Make sure the description is concise and aligns with the genre."
    )
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=20,
        temperature=0.7
    )
    return response.generations[0].text.strip()

def generate_music(lyrics, output_file="music"):
    duration = get_audio_duration("vocals.wav")
    music_prompt = generate_music_prompt(lyrics)
    # music_model.set_generation_params(duration=10)
    music_model.set_generation_params(duration=int(duration))
    wav = music_model.generate(descriptions=[music_prompt])
    audio_write(output_file, wav[0].cpu(), music_model.sample_rate)
    return output_file

def generate_vocals(lyrics, output_file="vocals.wav"):
    tts.tts_to_file(text=lyrics, speaker_wav="reference_voice.wav", language="en", file_path=output_file)
    return output_file

def merge_audio(vocals_file="vocals.wav", music_file="music.wav", output_file="final_song.wav"):
    vocals = AudioSegment.from_wav(vocals_file)
    music = AudioSegment.from_wav(music_file)
    
    if len(music) > len(vocals):  
        music = music[:len(vocals)]
    elif len(music) < len(vocals):
        loops = (len(vocals) // len(music)) + 1
        music = music * loops
        music = music[:len(vocals)]
    
    vocals = vocals - 5
    music = music - 3  
    
    final_mix = music.overlay(vocals, position=0)
    output_file = output_file.replace(".wav", ".mp3")  # Convert to MP3
    final_mix.export(output_file, format="mp3")  # Export as MP3
    return output_file

@app.route('/generate_song', methods=['POST'])
def generate_song():
    data = request.get_json()
    book_summary = data.get("book_summary")
    
    if not book_summary:
        return jsonify({"error": "No book summary provided"}), 400
    
    genre, lyrics = generate_lyrics(book_summary)
    generate_vocals(lyrics)
    generate_music(lyrics)
    final_song = merge_audio()

    # Return JSON with lyrics and downloadable MP3 file
    return jsonify({
        "lyrics": lyrics,
        "genre": genre,
        "download_url": f"/download_song?file={final_song}"
    })

@app.route('/download_song', methods=['GET'])
def download_song():
    file = request.args.get("file")
    
    if not file or not os.path.exists(file):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(file, as_attachment=True, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)