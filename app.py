from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import tempfile
import os
import librosa
import whisper
from sarcasm_classifier import predict_sarcasm
from feature_extractor import extract_features
import base64
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Whisper model
logger.info("Loading Whisper model...")
whisper_model = whisper.load_model("base", device="cpu", download_root="./models")
whisper_model.eval()  # Set to evaluation mode
logger.info("Whisper model loaded successfully")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_data')
def handle_audio_data(data):
    try:
        logger.debug("Received audio data")
        
        # Decode base64 audio data
        audio_data = base64.b64decode(data['audio'].split(',')[1])
        logger.debug("Decoded audio data")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        logger.debug(f"Saved audio to temporary file: {temp_file_path}")

        # Process audio
        # Transcribe audio
        logger.debug("Starting audio transcription...")
        transcription = whisper_model.transcribe(temp_file_path)
        text = transcription["text"]
        logger.debug(f"Transcription completed: {text}")

        # Extract features
        logger.debug("Extracting audio features...")
        y, sr = librosa.load(temp_file_path, sr=16000)
        features = extract_features(y, sr)
        logger.debug("Audio features extracted successfully")

        # Predict sarcasm
        logger.debug("Predicting sarcasm...")
        sarcasm_score = predict_sarcasm(text, features)
        logger.debug(f"Sarcasm score: {sarcasm_score}")

        # Clean up
        os.unlink(temp_file_path)
        logger.debug("Temporary file cleaned up")

        # Send results back to client
        result = {
            'text': text,
            'sarcasm_score': sarcasm_score,
            'features': {
                'pitch': float(features['pitch']),
                'energy': float(features['energy']),
                'zero_crossing_rate': float(features['zero_crossing_rate']),
                'spectral_centroid': float(features['spectral_centroid'])
            }
        }
        logger.debug(f"Sending results: {result}")
        emit('analysis_result', result)

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    logger.info("Starting server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 