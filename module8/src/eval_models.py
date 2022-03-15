from data_cleaner import load_dataset

import timeit
import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from tensorflow.keras.experimental import LinearModel

def signaltonoise(a, axis=0, ddof=0, ret_db=False):
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
    return np.linalg.norm(a - b)**2

def eval_time(model, x_test, test_runs=10):
    t = timeit.timeit(lambda: model.predict(x_test), number=test_runs)
    t = t / test_runs
    print(f'INFO. Average execution time for {test_runs} runs: {t:.3f} s')
    return t

def main():
    fr = '16k'

    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

    # filename = os.path.join(data_dir, f'{fr}.npy')
    # dataset = np.load(filename, allow_pickle=True).item()
    # frame_rate = dataset['frame_rate']
    # x_train, y_train = dataset['x_train'], dataset['y_train']
    # x_test, y_test = dataset['x_test'], dataset['y_test']

    # np.savez_compressed(os.path.join(data_dir, f'{fr}.npz'), frame_rate=frame_rate,
    #     x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)


    filename = os.path.join(data_dir, f'{fr}.npz')
    x_train, y_train, x_test, y_test = load_dataset(filename)

    epochs = 10
    model = LinearModel(units=y_test.shape[-1])
    model.compile(optimizer='adam', loss='mse')
    # model.fit(x_train, y_train, epochs=epochs)

    y_pred = model.predict(x_test)
    print(y_pred.shape)

    # y = y_test[0]
    # y_p = y_pred[0]

    # num_runs = 10
    # # print('time:', timeit.timeit(lambda: model.predict(x_test), number=num_runs) / num_runs)

    # eval_time(model, x_test, test_runs=5)

    # print(mse(y_pred, y_test))
    # graph_spectrogram(np.abs(y - y_p), show=False)


    x = x_train[0]
    y = y_train[0]

    plt.plot(x)
    plt.plot(y)
    plt.show()

    # print(signaltonoise(x, ret_db=True))
    # print(signaltonoise(y, ret_db=True))

    # print(signaltonoise(x_train, axis=1))
    # print(signaltonoise(y_train, axis=1))

    # print(np.all(signaltonoise(x_train, axis=1) > signaltonoise(y_train, axis=1)) == True)

    # graph_spectrogram(np.abs(x - y), show=False)
    # print((graph_spectrogram(y) - graph_spectrogram(y)).mean())
    # print(mse(graph_spectrogram(x), graph_spectrogram(y)))
    # print(mse(x, y))

if __name__ == '__main__':
    main()