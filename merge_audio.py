from pydub import AudioSegment

def merge_audio(vocals_file="vocals.wav", music_file="music.wav", output_file="final_song.wav"):
    vocals = AudioSegment.from_wav(vocals_file)
    music = AudioSegment.from_wav(music_file)

    # Adjust volume if needed
    vocals = vocals - 5  # Reduce volume by 5 dB
    music = music - 3  

    # Overlay vocals on music
    final_mix = music.overlay(vocals, position=0)

    # Export final song
    final_mix.export(output_file, format="wav")
    return output_file

if __name__ == "__main__":
    merge_audio()

