import numpy as np
import librosa
import torch

def extract_features(audio_chunk: np.ndarray, sr: int = 16000) -> dict:
    """Extract pitch and energy from a mono audio chunk."""
    y = audio_chunk.flatten()
    
    # RMS energy
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)
    energy = float(np.mean(rms))

    # Pitch via piptrack
    pitches, mags = librosa.piptrack(y=y, sr=sr, hop_length=512)
    pitch_vals = pitches[mags > np.median(mags)]
    pitch = float(np.mean(pitch_vals)) if pitch_vals.size > 0 else 0.0

    # Additional features
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y=y)
    zero_crossing_rate = float(np.mean(zcr))

    # Spectral centroid
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid = float(np.mean(cent))

    return {
        'pitch': pitch,
        'energy': energy,
        'zero_crossing_rate': zero_crossing_rate,
        'spectral_centroid': spectral_centroid,
        'emotion': 'neutral'  # Default emotion since we're not using SpeechBrain
    } 