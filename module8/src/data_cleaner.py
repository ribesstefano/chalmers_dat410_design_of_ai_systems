import os
from pydub import AudioSegment
import numpy as np
import warnings

from audio_utils import *

warnings.filterwarnings('ignore')

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def printProgressBar(iteration, total, prefix='Progress:', suffix='Complete',
                     decimals=1, length=50, fill='█', printEnd='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / total))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def split_np(x, perc):
    perc_size = int(x.shape[0] * perc)
    return x[:perc_size, :], x[perc_size:, :]

def load_dataset(filename, reshape=False):
    """
    Loads a dataset into numpy arrays of default shape: (N, F * S), where N is
    the batch size, F the frame rate and S the audio length in seconds. If
    reshape=True, then the returned datasets will have shape: (N, F, S) instead.
    
    :param      filename:  The filename of the npy file
    :type       filename:  str
    :param      reshape:   Whether to return data of shape: (N, F, S)
    :type       reshape:   bool
    
    :returns:   x_train, y_train, x_test, y_test
    :rtype:     Tuple of Numpy arrays
    """
    dataset = np.load(filename, allow_pickle=True).item()
    frame_rate = dataset['frame_rate']
    x_train, y_train = dataset['x_train'], dataset['y_train']
    x_test, y_test = dataset['x_test'], dataset['y_test']
    if reshape:
        def reshape_np(x):
            return np.reshape(x, (-1, frame_rate, x.shape[-1] // frame_rate))
        x_train, y_train = reshape_np(x_train), reshape_np(y_train)
        x_test, y_test = reshape_np(x_test), reshape_np(y_test)
    return x_train, y_train, x_test, y_test

def main():
    # ==========================================================================
    # Dataset Parameters
    # ==========================================================================
    frame_rate = 16000 # 48000
    background_attenuation = 0 # 20
    ms_pad = 2000 # The final length of the audio clip, either trimmed or padded
    background_trim_len = 4000 # The final length of the background clip
    pcm = 16 # Dynamic range (in bit)
    train_perc = 0.8
    background_type = 'background_2.wav'
    # ==========================================================================
    # Directories
    # ==========================================================================
    fr = f'{frame_rate // 1000}k'
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    audio_dir = os.path.join(data_dir, fr)
    trim_dir = os.path.join(data_dir, f'{fr}_trimmed_audio')
    trim_background_dir = os.path.join(data_dir, f'{fr}_trimmed+background_audio')
    trim_clean_dir = os.path.join(data_dir, f'{fr}_trimmed_clean_audio')
    mkdir(trim_dir)
    mkdir(trim_background_dir)
    mkdir(trim_clean_dir)
    # ==========================================================================
    # Trim and pad all audio data to 2000ms
    # ==========================================================================
    print('DEBUG. Trimming and padding audio files (the slowest process).')
    wav_files = []
    for path, subdirs, files in os.walk(audio_dir):
        for filename in files:
            if filename.endswith('wav'):
                wav_files.append(os.path.join(path, filename))
    # Loop over all wav files in data directory and save them in output dir
    for i, wav_file in enumerate(wav_files):
        outfile = os.path.join(trim_dir, str(i) + '.wav')
        preprocess_audio(wav_file, outfile, ms_pad, frame_rate)
        printProgressBar(i, len(wav_files))
    # ==========================================================================
    # Overlap audio over background noise and generate corresponding clean data
    # ==========================================================================
    print(f'DEBUG. Generating Noisy and Clean audio clips.')
    background_file = os.path.join(data_dir, 'backgrounds', background_type)
    # Make background quieter by setting an attenuation level (in dB)
    background = AudioSegment.from_wav(background_file)
    background = background - background_attenuation
    # Loop over files and add spoken audio in a random place on the background
    for i, filename in enumerate(os.listdir(trim_dir)):
        # Setup file names
        infile = os.path.join(trim_dir, filename)
        noisy_outfile = os.path.join(trim_background_dir, filename)
        clean_outfile = os.path.join(trim_clean_dir, filename)
        # Read audio file
        audio_clip = AudioSegment.from_wav(infile)
        # Process audio files
        a = overlap_noise(audio_clip, background, ms_pad, background_trim_len,
                          frame_rate)
        noisy_audio, clean_audio = a
        wav2file(noisy_audio, noisy_outfile)
        wav2file(clean_audio, clean_outfile)
        printProgressBar(i, len((os.listdir(trim_dir))))
    # ==========================================================================
    # Generate npy tarballs
    # ==========================================================================
    print('DEBUG. Converting audio files to Numpy.')
    x_data = []
    y_data = []
    print('DEBUG. Converting clean audio files to Numpy.')
    for i, filename in enumerate(os.listdir(trim_clean_dir)):
        if filename.endswith('wav'):
            y_data.append(wav2numpy(os.path.join(trim_clean_dir, filename)))
            printProgressBar(i + 1, len((os.listdir(trim_clean_dir))))
    print('DEBUG. Converting noisy audio files to Numpy.')
    for i, filename in enumerate(os.listdir(trim_background_dir)):
        if filename.endswith('wav'):
            x_data.append(wav2numpy(os.path.join(trim_background_dir, filename)))
            printProgressBar(i + 1, len((os.listdir(trim_dir))))
    x_train, x_test = split_np(np.array(x_data), train_perc)
    y_train, y_test = split_np(np.array(y_data), train_perc)
    dataset = {
        'frame_rate' : frame_rate,
        'x_train' : x_train,
        'y_train' : y_train,
        'x_test' : x_test,
        'y_test' : y_test,
    }
    np.save(os.path.join(data_dir, f'{fr}.npy'), dataset)
    # ==========================================================================
    # Load dataset (Testing)
    # ==========================================================================
    dataset = load_dataset(os.path.join(data_dir, f'{fr}.npy'), reshape=True)
    x_train, y_train, x_test, y_test = dataset
    print('x_train.shape', x_train.shape)
    # ==========================================================================
    # Writing Numpy array to WAV file (Testing)
    # ==========================================================================
    print('x_train.shape', x_train.shape)
    x = os.path.join(data_dir, 'x.wav')
    y = os.path.join(data_dir, 'y.wav')
    print('x_train[5].shape: ', x_train[5].shape)
    numpy2wav(x_train[5], x, frame_rate)
    numpy2wav(y_train[5], y, frame_rate)

if __name__ == '__main__':
    main()