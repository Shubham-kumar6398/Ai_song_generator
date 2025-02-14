import streamlit as st
import torch
from TTS.api import TTS
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from pydub import AudioSegment
import cohere
import os

# Initialize Cohere API
COHERE_API_KEY = "r9uX1zwVave9HWB9FoY4AITKVd12BefKQ3hVWfw5"
co = cohere.Client(COHERE_API_KEY)

# Load models
music_model = MusicGen.get_pretrained('facebook/musicgen-small')
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

def generate_lyrics(book_summary, genre):
    prompt = (
        f"Write a complete song based on this book summary: {book_summary}. "
        f"The song should follow the {genre} style. Ensure that all verses, chorus, "
        f"and bridge are complete and do not end mid-line. Use the following format:\n\n"
        "Verse 1:\n[Complete lyrics here]\n\n"
        "Chorus:\n[Complete lyrics here]\n\n"
        "Verse 2:\n[Complete lyrics here]\n\n"
        "Bridge:\n[Complete lyrics here]\n\n"
        "Chorus:\n[Repeat with variations]\n\n"
        "Outro:\n[Closing lyrics that provide a satisfying ending]"
    )
    response = co.generate(model="command-xlarge-nightly", prompt=prompt, max_tokens=1000, temperature=0.8)
    return response.generations[0].text.strip()

def generate_vocals(lyrics, output_file="vocals.wav"):
    tts.tts_to_file(text=lyrics, speaker_wav="reference_voice.wav", language="en", file_path=output_file)
    return output_file

# def generate_music(prompt, duration=30, output_file="music.wav"):
#     music_model.set_generation_params(duration=duration)
#     wav = music_model.generate(descriptions=[prompt])
#     audio_write(output_file, wav[0].cpu(), music_model.sample_rate)
#     return output_file

# def merge_audio(vocals_file="vocals.wav", music_file="music.wav", output_file="final_song.wav"):
#     vocals = AudioSegment.from_wav(vocals_file) - 5
#     music = AudioSegment.from_wav(music_file) - 3
#     final_mix = music.overlay(vocals, position=0)
#     final_mix.export(output_file, format="wav")
    # return output_file

# Streamlit UI
st.title("AI Song Generator 🎶")
book_summary = st.text_area("Enter a book summary:")
genre = st.selectbox("Select Genre", ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical"])
lyrics = ""
user_lyrics = ""

# Generate Lyrics
if st.button("Generate Lyrics"):
    if book_summary:
        lyrics = generate_lyrics(book_summary, genre)
        st.text_area("Generated Lyrics", lyrics, height=300)

# Allow user to enter or edit lyrics only if generated lyrics exist
if lyrics:
    user_lyrics = st.text_area("Enter Lyrics:", value=lyrics, height=200)

# Show "Generate Vocals" button only if user_lyrics is not empty
if user_lyrics.strip():  # Ensure user_lyrics is not just whitespace
    if st.button("Generate Vocals"):
        vocal_file = generate_vocals(user_lyrics)
        st.success("Vocal successfully generated!")
        st.audio(vocal_file, format='audio/wav')


# if st.button("Generate Music"):
#     if genre:
#         music_prompt = f"A {genre.lower()} instrumental background track."
#         music_file = generate_music(music_prompt)
#         st.success("Music successfully generated!")
#         st.audio(music_file, format='audio/wav')
#     else:
#         st.warning("Please select a genre.")

# if st.button("Merge Vocals & Music"):
#     if os.path.exists("vocals.wav") and os.path.exists("music.wav"):
#         final_song = merge_audio()
#         st.success("Final song generated!")
#         st.audio(final_song, format='audio/wav')
#         st.download_button("Download Final Song", final_song, file_name="final_song.wav")
#     else:
#         st.warning("Please generate vocals and music first.")
