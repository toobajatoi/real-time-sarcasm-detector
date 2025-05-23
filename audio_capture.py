import sounddevice as sd
import numpy as np
import whisper
# import openai  # or Deepgram client

SAMPLE_RATE = 16000
CHUNK_DURATION = 1.0  # seconds
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_DURATION)

# Load Whisper once
_model = whisper.load_model("base")

def stream_audio_chunks():
    """Yields raw audio chunks (np.float32 mono) of fixed duration."""
    buffer = np.empty((0, 1), dtype=np.float32)

    def callback(indata, frames, time, status):
        nonlocal buffer
        if status:
            print(f"Audio status: {status}")
        buffer = np.concatenate((buffer, indata), axis=0)

    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, dtype='float32', callback=callback):
        while True:
            if buffer.shape[0] >= CHUNK_SAMPLES:
                chunk = buffer[:CHUNK_SAMPLES]
                buffer = buffer[CHUNK_SAMPLES:]
                yield chunk

def transcribe(audio_chunk: np.ndarray) -> str:
    """Run Whisper on raw audio and return text."""
    # Whisper expects a 1D float32 array
    audio_np = audio_chunk.flatten()
    result = _model.transcribe(audio_np, fp16=False)
    return result.get("text", "").strip()

    # e.g. response = openai.Audio.transcriptions.create(...)
    # return response['text']
    return "I'm sooo happy for you"  # placeholder 