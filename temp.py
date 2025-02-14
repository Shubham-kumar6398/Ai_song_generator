import torch
import os
from TTS.api import TTS
from subprocess import run

# Load the TTS model for initial vocal generation
torch.serialization.default_load_weights_only = False
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")  # Use "cuda" if available

# Generate spoken vocals first
def generate_vocals(lyrics, output_file="vocals_tts.wav"):
    tts.tts_to_file(text=lyrics, speaker_wav="reference_voice.wav", language="en", file_path=output_file)
    return output_file

# Convert spoken vocals into singing vocals using So-VITS-SVC
def convert_to_singing(input_vocal="vocals_tts.wav", output_vocal="vocals_singing.wav", model_path="so_vits_svc_model.pth"):
    """ Converts spoken vocals into a singing style """
    cmd = f"python inference.py --input {input_vocal} --output {output_vocal} --model {model_path} --pitch_shift 2"
    run(cmd, shell=True)  # Calls So-VITS-SVC to process vocals
    return output_vocal

# Generate instrumental music (optional, using Meta’s MusicGen)
def generate_music(prompt="rock song for Atomic Habits", output_music="music.wav"):
    cmd = f"python generate_music.py --prompt '{prompt}' --output {output_music}"
    run(cmd, shell=True)  # Calls an AI music generator
    return output_music

# Merge the generated singing vocals with the music
def merge_audio(vocals="vocals_singing.wav", music="music.wav", output="final_song.wav"):
    cmd = f"ffmpeg -i {vocals} -i {music} -filter_complex amix=inputs=2:duration=first:dropout_transition=2 {output}"
    run(cmd, shell=True)  # Calls FFmpeg to mix audio files
    return output

if __name__ == "__main__":
    lyrics = """In the quest for self-improvement, a journey so profound,
Atomic Habits, a guide, to where success is found.
Small changes, consistent steps, a powerful force,
James Clear, the mastermind, unlocking the success course.

Rock your habits, make them stick,
Small actions, big impact, don't be quick to quit.
Design your path, one step at a time,
Breakthrough the barriers, a new you to find."""

    # Step 1: Generate spoken vocals
    spoken_vocals = generate_vocals(lyrics)

    # Step 2: Convert spoken vocals into singing
    singing_vocals = convert_to_singing(spoken_vocals)

    # Step 3: Generate background music
    music_file = generate_music()

    # Step 4: Merge singing vocals and music
    final_song = merge_audio(singing_vocals, music_file)

    print(f"Final song saved as {final_song}")
