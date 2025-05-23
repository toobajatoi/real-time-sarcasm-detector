# Real-Time Sarcasm Detector

A real-time sarcasm detection system that analyzes speech patterns and audio features to identify sarcastic tones in conversations.

## Project Overview

This project implements a real-time sarcasm detection system using machine learning and audio processing techniques. It captures audio input, extracts relevant features, and uses a trained model to classify whether the speech contains sarcasm.

### Key Features
- Real-time audio capture and processing
- Feature extraction from audio signals
- Sarcasm classification using machine learning
- Web-based dashboard for visualization
- Real-time results display

## Architecture

The system consists of several key components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Audio Capture  │────▶│Feature Extraction│────▶│Sarcasm Classifier│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────────────────────────────────────────────────────┐
│                      Web Dashboard                            │
└───────────────────────────────────────────────────────────────┘
```

### Components:
1. **Audio Capture** (`audio_capture.py`)
   - Handles real-time audio recording
   - Manages audio stream processing

2. **Feature Extraction** (`feature_extractor.py`)
   - Extracts relevant audio features
   - Processes audio signals for analysis

3. **Sarcasm Classifier** (`sarcasm_classifier.py`)
   - Implements the ML model for sarcasm detection
   - Processes features and makes predictions

4. **Web Interface** (`app.py`, `templates/`, `static/`)
   - Flask-based web application
   - Real-time visualization of results

## Setup & Run Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/toobajatoi/real-time-sarcasm-detector.git
cd real-time-sarcasm-detector
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Demo Instructions

1. Click the "Start Recording" button on the web interface
2. Speak into your microphone
3. The system will process your speech in real-time
4. Results will be displayed on the dashboard showing:
   - Sarcasm probability
   - Audio waveform
   - Classification results

### Test Examples

Try these example phrases to test the system:
- "Oh great, another meeting" (sarcastic)
- "I love waiting in line" (sarcastic)
- "The weather is nice today" (non-sarcastic)
- "I'm really happy to help" (non-sarcastic)

## Dependencies

All required dependencies are listed in `requirements.txt`. Key packages include:
- Flask and Flask-SocketIO for web interface
- PyTorch and Transformers for ML model
- Librosa and SoundDevice for audio processing
- OpenAI Whisper for speech recognition
- Other utility packages for data processing and visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 