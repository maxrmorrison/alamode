# alamode
Synthetic multimodal audio database generator

Alamode is a tool for creating controlled experimental conditions in order to
analyze properties of algorithms for generating audio. Alamode can synthesize
four types of audio signals:
- Sine waves with random frequency
- Square waves with random frequency
- Clicks with random location
- White noise

Alamode can also output normalize log-melspectrograms, which can be immediately
used for training a machine learning model.

### Installation
```
git clone <repo>
cd alamode
pip install .
```

### Usage
```
usage: alamode.py [-h] [-d DURATION] [-l] [-n NUM] [-o OUTPUT] [-r SAMPLING_RATE] sound

positional arguments:
  sound                 The type of sound to generate

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        The length in seconds of generated audio
  -l, --logmel          Whether to also generate the log-melspectrograms
  -n NUM, --num NUM     The number of samples to generate
  -o OUTPUT, --output OUTPUT
                        The directory to place output
  -r SAMPLING_RATE, --sampling_rate SAMPLING_RATE
                        The audio sampling rate
```                        