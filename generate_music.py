import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('facebook/musicgen-small')

def generate_music(prompt, duration=30, output_file="music"):
    model.set_generation_params(duration=duration)
    wav = model.generate(descriptions=[prompt])
    audio_write(output_file, wav[0].cpu(), model.sample_rate)
    return output_file

if __name__ == "__main__":
    prompt = "A hip-hop beat with deep bass."
    generate_music(prompt)
