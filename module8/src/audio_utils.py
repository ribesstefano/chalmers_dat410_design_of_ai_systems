import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import random

def wav2file(x, filename):
    # Export as wav (convert to mono-channel if neccessary, see ffmpeg docs)
    x.export(filename, format='wav', parameters=['-ac', '1'])

def wav2numpy(filename):
    samplerate, data = wavfile.read(filename)
    return np.array(data, dtype=float)

def scale(x, pcm=16):
    return np.int16(x / np.max(np.abs(x)) * (2**(pcm-1)-1))

def numpy2wav(x, filename, frame_rate=16000, pcm=16):
    fr = x.shape[1] if len(x.shape) > 1 else frame_rate
    scaled = scale(x.flatten(), pcm) if len(x.shape) > 1 else scale(x, pcm)
    wavfile.write(filename, fr, scaled)

def preprocess_audio(filename, outfile, ms_pad=2000, frame_rate=16000):
    # Trim or pad audio segment to ms_pad ms
    padding = AudioSegment.silent(duration=ms_pad)
    segment = AudioSegment.from_wav(filename)[:ms_pad]
    segment = padding.overlay(segment)
    # Set frame rate
    segment = segment.set_frame_rate(frame_rate)
    wav2file(segment, outfile)

# Used to standardize volume of audio clip
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def overlap_noise(audio, background, ms_pad=2000, background_trim_len=4000,
                  frame_rate=16000):
    # Get random positions within the total length
    back_pos = random.randint(0, len(background) - background_trim_len - 1)
    audio_pos = random.randint(0, background_trim_len - ms_pad - 1)
    # Generate noisy audio
    background_clip = background[back_pos:back_pos+background_trim_len]
    noisy_audio = background_clip.overlay(audio, position=audio_pos)
    noisy_audio = noisy_audio.set_frame_rate(frame_rate)
    noisy_audio = noisy_audio.set_channels(1)
    # Generate clean audio
    silence = AudioSegment.silent(duration=background_trim_len)
    clean_audio = silence.overlay(audio, position=audio_pos)
    clean_audio = clean_audio.set_frame_rate(frame_rate)
    # print('noisy_audio:', noisy_audio.frame_rate, noisy_audio.channels)
    # print('clean_audio:', clean_audio.frame_rate, clean_audio.channels)
    return noisy_audio, clean_audio