import os
import re
import matplotlib.pyplot as plt
import numpy as np

def norm(a):
    x = np.array(a)
    return (x - x.min()) / (x.max() - x.min())

def plot_timings():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
    log_file = os.path.join(data_dir, 'evaluation.log')
    regex_time = re.compile(r'.*data/waveform_(.*)\.pdf.*Average execution time for ([0-9]*) runs: ([0-9\.]*) s')

    models = []
    timings = []

    with open(log_file) as f:
        for line in f:
            match = regex_time.match(line)
            if match is not None:
                print(f'INFO. [{match.group(1)}] {match.group(3)} s')
                if 'conv' in match.group(1):
                    models.append(match.group(1))
                    timings.append(float(match.group(3)))

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = np.arange(len(timings))

    plt.bar(index + bar_width, (timings), bar_width)
    plt.xticks(index + bar_width, models, rotation=-90)

    # plt.yscale('log')
    plt.ylabel('Execution Time [s]')
    plt.title('Convolutional Model Execution Time')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plot_mse():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
    log_file = os.path.join(data_dir, 'evaluation_snr.log')

    regex = re.compile(r'.*data/waveform_(.*)\.pdf.*: ([\-0-9\.]*).*')

    models = []
    values = []

    with open(log_file) as f:
        for line in f:
            match = regex.match(line)
            if match is not None:
                print(f'INFO. [{match.group(1)}] {match.group(2)} s')
                if 'MSE' in line:
                    models.append(match.group(1))
                    values.append(float(match.group(2)))

    fig, ax = plt.subplots()
    bar_width = 0.35 * 2
    index = np.arange(len(values))

    plt.bar(index + bar_width, (values), bar_width, zorder=2, color='green')
    plt.xticks(index + bar_width, models, rotation=-90)

    plt.yscale('log')
    plt.ylabel('MSE')
    plt.title('Average MSE for Linear and Convolutional models')
    plt.grid(which='both', axis='y', alpha=0.7, zorder=1)
    plt.tight_layout()
    plt.savefig('mse.pdf')
    plt.show()

def plot_snr_y_pred():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
    log_file = os.path.join(data_dir, 'evaluation_snr.log')

    regex = re.compile(r'.*data/waveform_(.*)\.pdf.*: ([\-0-9\.]*).*')

    models = []
    values = []

    with open(log_file) as f:
        for line in f:
            match = regex.match(line)
            if match is not None:
                print(f'INFO. [{match.group(1)}] {match.group(2)} s')
                if 'SNR_dB(y_pred)' in line:
                    models.append(match.group(1))
                    values.append(float(match.group(2)))

    fig, ax = plt.subplots()
    bar_width = 0.35 * 2
    index = np.arange(len(values))

    plt.bar(index + bar_width, values, bar_width, zorder=2, color='orange')
    plt.xticks(index + bar_width, models, rotation=-90)

    # plt.yscale('log')
    plt.ylabel('SNR [dB]')
    plt.title('Average SNR of the denoised signals')
    plt.grid(which='both', axis='y', alpha=0.7, zorder=1)
    plt.tight_layout()
    plt.savefig('snr_y_pred.pdf')
    plt.show()

def plot_snr():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
    log_file = os.path.join(data_dir, 'evaluation_snr.log')

    regex = re.compile(r'.*data/waveform_(.*)\.pdf.*: ([\-0-9\.]*).*')

    models = []
    snr_y = []
    snr_y_pred = []

    with open(log_file) as f:
        for line in f:
            match = regex.match(line)
            if match is not None:
                print(f'INFO. [{match.group(1)}] {match.group(2)} s')
                if 'SNR_dB(y_pred)' in line:
                    models.append(match.group(1))
                    snr_y_pred.append(float(match.group(2)))
                if 'SNR_dB(y)' in line:
                    snr_y.append(float(match.group(2)))

    fig, ax = plt.subplots()
    bar_width = 0.35 * 2
    index = np.arange(len(snr_y_pred))

    snr = np.array(snr_y) - np.array(snr_y_pred)

    plt.bar(index + bar_width, snr, bar_width, zorder=2, color='orange')
    plt.xticks(index + bar_width, models, rotation=-90)

    # plt.yscale('log')
    plt.ylabel('SNR [dB]')
    plt.title('Average SNR difference of the denoised signals')
    plt.grid(which='both', axis='y', alpha=0.7, zorder=1)
    plt.tight_layout()
    plt.savefig('snr.pdf')
    plt.show()

if __name__ == '__main__':
    # plot_timings()
    # plot_mse()
    # plot_snr_y_pred()
    plot_snr()