import librosa
import numpy as np

def extract_features(path):
    y, sr = librosa.load(path, mono=True, duration=20)
    return {
        "chroma_stft": np.mean(librosa.feature.chroma_stft(y=y, sr=sr)),
        "spec_cent": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        "spec_bw": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
        "rolloff": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
        "zcr": np.mean(librosa.feature.zero_crossing_rate(y=y)),
        "mfcc": np.mean(librosa.feature.mfcc(y=y, sr=sr))
    }
