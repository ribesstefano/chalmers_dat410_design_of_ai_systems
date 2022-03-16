from data_cleaner import load_dataset
import linear_model
import conv1d_model
# import rnn_model

import timeit
import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from tensorflow.keras.experimental import LinearModel
import itertools

def signaltonoise(a, axis=0, ddof=0, ret_db=False, sd=None):
    """
    The signal-to-noise ratio of the input data.
    Returns the signal-to-noise ratio of `a`, here defined as the mean
    divided by the standard deviation.
    Parameters
    ----------
    a : array_like
        An array_like object containing the sample data.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    ddof : int, optional
        Degrees of freedom correction for standard deviation. Default is 0.
    Returns
    -------
    s2n : ndarray
        The mean to standard deviation ratio(s) along `axis`, or 0 where the
        standard deviation is 0.
    """
    a = np.asanyarray(a)
    m = a.mean(axis)
    if sd is None:
        sd = a.std(axis=axis, ddof=ddof)
    snr = np.where(sd == 0, 0, m / sd)
    if ret_db:
        return 20 * np.log10(np.abs(snr))
    else:
        return snr

# Calculate and plot spectrogram for a wav audio file
def graph_spectrogram(data=None, wav_file='', show=False):
    if data is None:
        _, data = wavfile.read(wav_file)
    nfft = 200 # Length of each window segment
    fs = 8000 # Sampling frequencies
    noverlap = 120 # Overlap between windows
    nchannels = data.ndim
    if nchannels == 1:
        pxx, freqs, bins, im = plt.specgram(data, nfft, fs, noverlap=noverlap)
    elif nchannels == 2:
        pxx, freqs, bins, im = plt.specgram(data[:,0], nfft, fs, noverlap=noverlap)
    if show:
        plt.show()
    return pxx

def mse(a, b):
    batch_size = a.shape[0]
    x = np.reshape(a, (batch_size, -1))
    y = np.reshape(b, (batch_size, -1))
    return (np.linalg.norm(x - y, axis=1)**2).mean()

def eval_time(model, x_test, test_runs=10, design_name=''):
    t = timeit.timeit(lambda: model.predict(x_test), number=test_runs)
    t = t / test_runs
    print(f'INFO. [{design_name}] Average execution time for {test_runs} runs: {t:.3f} s')
    return t

def eval_model(model, x_test, y_test, input_transposed=True, test_runs=10, plot_name=None):
    y_pred = model.predict(x_test)

    if len(y_test.shape) > 2:
        if input_transposed:
            x = x_test.transpose(0, 2, 1)
            y = y_test.transpose(0, 2, 1)
            y_p = y_pred.transpose(0, 2, 1)
        else:
            x = x_test
            y = y_test
            y_p = y_pred
        flatten_shape = (-1, *y_p[0].flatten().shape)
        x = np.reshape(x, flatten_shape)
        y = np.reshape(y, flatten_shape)
        y_p = np.reshape(y_p, flatten_shape)
    else:
        x = x_test
        y = y_test
        y_p = y_pred

    e = mse(y, y_p)

    noise_power = ((x - y)**2).mean(axis=1)
    noise_std = (x - y).std(axis=1)
    x_power = (x**2).mean(axis=1)
    y_power = (y**2).mean(axis=1)
    y_p_power = (y_p**2).mean(axis=1)

    # NOTE: For y, the noise has expected value of 0, therefore we use the noise std instead
    y_snr = (y_power / noise_std).mean() # signaltonoise(y, axis=1, ret_db=True, sd=noise_sd).mean()
    x_snr = (x_power / noise_power).mean() # signaltonoise(x, axis=1, ret_db=True, sd=noise_sd).mean()
    y_p_snr = (y_p_power / noise_power).mean() # signaltonoise(y_p, axis=1, ret_db=True, sd=noise_sd).mean()

    print(f'INFO. [{plot_name}] avg. MSE: {e:.1f}')
    print(f'INFO. [{plot_name}] avg. SNR_dB(x): {x_snr:.2f}')
    print(f'INFO. [{plot_name}] avg. SNR_dB(y): {y_snr:.2f}')
    print(f'INFO. [{plot_name}] avg. SNR_dB(y_pred): {y_p_snr:.2f}')
    # eval_time(model, x_test, test_runs, plot_name)

    plt.plot(y[0].flatten(), label='Clean Audio', color='blue')
    plt.plot(y_p[0].flatten(), label='Predicted Audio', color='darkorange', alpha=0.7)
    plt.plot(x[0].flatten(), label='Noise Audio', color='green', alpha=0.6)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title(os.path.basename(plot_name).rsplit('.', 1)[0])
    plt.legend()
    # plt.show()
    plt.savefig(plot_name)
    plt.clf()
    # _ = graph_spectrogram(y[0].flatten(), show=True)
    # _ = graph_spectrogram(y_p[0].flatten(), show=True)
    # _ = graph_spectrogram(np.abs(y[0].flatten() - y_p[0].flatten()), show=True)


def plot_history(history, filename):
    if history is not None:
        plt.plot(history.history['mse'])
        plt.plot(history.history['val_mse'])
        plt.title('Model MSE')
        plt.ylabel('MSE')
        plt.xlabel('Epochs')
        plt.legend(['Train loss', 'Validation loss'], loc='lower left')
        plt.title(os.path.basename(filename).rsplit('.', 1)[0])
        plt.grid()
        plt.savefig(filename)
        plt.clf()

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

    training_epochs = 10
    models = {
        'linear' : linear_model.train_model,
        'conv1d' : conv1d_model.train_model,
        # 'rnn' : rnn_model.train_model,
    }
    noises = ['wind_at_sea', 'white']
    noise_gains = [0, 5, 10]
    frame_rates = [8000, 16000]
    design_points = list(itertools.product(models.keys(), frame_rates, noises, noise_gains))

    for design_point in design_points:
        model_id, frame_rate, noise, noise_gain = design_point
        design_name = f'{frame_rate // 1000}k_{noise}_{noise_gain}dB'
        model_filename = os.path.join(data_dir, f'{model_id}_{design_name}')
        npz_filename = os.path.join(data_dir, design_name + '.npz')
        print(f'INFO. Running evaluation for {design_name}.')
        # Training
        train_model = models[model_id]
        training = train_model(npz_filename, model_filename, epochs=training_epochs)
        model, x_test, y_test, input_transposed, history = training
        # Evaluation (actual tests)
        plot_name = f'waveform_{model_id}_{design_name}.pdf'
        plot_name = os.path.join(data_dir, plot_name)
        eval_model(model, x_test, y_test, input_transposed, plot_name=plot_name)
        # Plot training and validation loss
        plot_name = f'loss_{model_id}_{design_name}.pdf'
        plot_name = os.path.join(data_dir, plot_name)
        plot_history(history, plot_name)

if __name__ == '__main__':
    main()