import streamlit as st
import streamlit_webrtc as webrtc
import tempfile
import os
from pathlib import Path

st.title("Audio Recorder Test")

# Initialize the audio recorder
audio_recorder = webrtc.audio_recorder(
    key="audio_recorder",
    mode=webrtc.AudioRecorderMode.RECORDING,
    sample_rate=16000,
)

if audio_recorder.audio_data is not None:
    # Save the recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file.write(audio_recorder.audio_data)
        temp_file_path = temp_file.name
    
    # Display audio player
    st.audio(audio_recorder.audio_data, format="audio/wav")
    
    # Display file information
    st.write("Audio saved to:", temp_file_path)
    st.write("File size:", len(audio_recorder.audio_data), "bytes")
    
    # Clean up the temporary file
    os.unlink(temp_file_path) 