import torch

# Override PyTorch's default behavior
torch.serialization.default_load_weights_only = False

from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")  # Use "cuda" if you have a GPU

def generate_vocals(lyrics, output_file="vocals.wav"):
    tts.tts_to_file(text=lyrics, speaker_wav="reference_voice.wav", language="en", file_path=output_file)
    return output_file

if __name__ == "__main__":
    lyrics = """In the quest for self-improvement, a journey so profound,
Atomic Habits, a guide, to where success is found.
Small changes, consistent steps, a powerful force,
James Clear, the mastermind, unlocking the success course.

Rock your habits, make them stick,
Small actions, big impact, don't be quick to quit.
Design your path, one step at a time,
Breakthrough the barriers, a new you to find.

Four laws, a roadmap, to navigate the change,
Make it obvious, attractive, and easy, a habit's range.
Reduce the friction, start with a simple plan,
Reinforce the positive, and take control, be the man!

Bad habits, they're no match, for the power you'll gain,
Reverse the laws, break free, and watch the old you fade.
Case studies, real-life proof, you'll never be the same,
Atomic Habits, the key, to unlock your inner flame.

Habits, they're atomic, a force so strong,
Build your system, embrace the change, sing this rockin' song.
Don't fear the journey, take that first stride,
Small habits, big results, a transformation inside.

So, let the habits ignite, a revolution of self,
Clear's wisdom, a guiding light, on the road to mental wealth.
Atomic Habits, the anthem, for a better you,
Rock on, and make those changes, it's what you've got to do!
"""
    generate_vocals(lyrics)
