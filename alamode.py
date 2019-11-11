import argparse
import os

import IPython.display as ipd
import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def timepoints(sampling_rate, duration):
    """Generates a grid of equally-spaced timepoints"""
    return np.linspace(0., duration, duration * sampling_rate)


def sine(sampling_rate, duration, amplitude=1.0):
    """Sine wave generator"""
    t = timepoints(sampling_rate, duration)
    f = np.random.uniform(20, sampling_rate / 2)
    return amplitude * np.sin(2 * np.pi * f * t)


def square(sampling_rate, duration, amplitude=1.0):
    """Square wave generator"""
    t = timepoints(sampling_rate, duration)
    f = np.random.uniform(20, sampling_rate / 2)
    return amplitude * signal.square(2 * np.pi * f * t)


def white_noise(sampling_rate, duration, amplitude=1.0):
    """White noise generator"""
    return np.random.normal(size=int(sampling_rate * duration))


def click(sampling_rate, duration, amplitude=1.0):
    """Click generator"""
    x = np.zeros(int(sampling_rate * duration))
    location = np.random.randint(2, len(x) - 3)
    x[location - 2: location + 2] = amplitude
    return x


def logmelspectrogram(signal, sampling_rate, time_bins=128, frequency_bins=256):
    """Transforms signal to log-melspectrogram"""
    spectrogram = librosa.melspectrogram(
        signal, sr=sampling_rate, n_mels=256,
        hop_size=sampling_rate / time_bins)
    
    # Fix maximum at 1
    spectrogram /= np.max(spectrogram)
    
    # Convert to log-scale
    spectrogram = librosa.power_to_db(spectrogram)
    
    # Remove silent bins
    spectrogram = spectrogram[spectrogram < -10] = 0
    
    # Rescale to (-1, 1)
    return (spectrogram + 5) / 5


def generate(sound, sampling_rate, duration, num, logmel, output):
    """Generates num variations of specified sound and saves to disk"""
    os.makedirs(output, exist_ok=True)
    
    # Select generator
    if sound == 'sine':
        generator = sine
    elif sound == 'square':
        generator = square
    elif sound == 'white_noise':
        generator = white_noise
    elif sound == 'click':
        generator = click
    else:
        raise ValueError('Selected sound {} is not implemented'.format(sound))
    
    for i in range(num):
        # Generate
        signal = generator(sampling_rate, duration)
        
        # Save audio
        filename = os.path.join(output, sound + '-' + format(i, '06d'))
        librosa.output.write_wav(filename + '.wav', signal, sampling_rate)
        
        if logmel:
            # Save spectrogram
            spectrogram = logmelspectrogram(signal, sampling_rate)
            np.save(filename + '.npy', spectrogram)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sound', help='The type of sound to generate')
    
    parser.add_argument(
        '-d', '--duration', type=float, default=1.0,
        help='The length in seconds of generated audio')
    parser.add_argument(
        '-l', '--logmel', type=lambda x: (str(x).lower() == 'true'),
        default=False, help='Whether to also generate the log-melspectrograms')
    parser.add_argument(
        '-n', '--num', type=1, default=1,
        help='The number of samples to generate')
    parser.add_argument('-o', '--output', default='.',
                        help='The directory to place output')
    parser.add_argument('-r', '--sampling_rate', type=int, default=16000,
                        help='The audio sampling rate')
    
    generate(**vars(parser.parse_args()))
    