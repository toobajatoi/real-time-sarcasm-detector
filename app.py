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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Whisper model
whisper_model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_data')
def handle_audio_data(data):
    try:
        # Decode base64 audio data
        audio_data = base64.b64decode(data['audio'].split(',')[1])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        # Process audio
        # Transcribe audio
        transcription = whisper_model.transcribe(temp_file_path)
        text = transcription["text"]

        # Extract features
        y, sr = librosa.load(temp_file_path, sr=16000)
        features = extract_features(y, sr)

        # Predict sarcasm
        sarcasm_score = predict_sarcasm(text, features)

        # Clean up
        os.unlink(temp_file_path)

        # Send results back to client
        emit('analysis_result', {
            'text': text,
            'sarcasm_score': sarcasm_score,
            'features': {
                'pitch': float(features['pitch']),
                'energy': float(features['energy']),
                'zero_crossing_rate': float(features['zero_crossing_rate']),
                'spectral_centroid': float(features['spectral_centroid'])
            }
        })

    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 