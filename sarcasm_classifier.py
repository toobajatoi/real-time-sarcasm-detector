from transformers import pipeline

# Load a sarcasm-detection pipeline once
_sarcasm_pipe = pipeline(
    "text-classification",
    model="helinivan/english-sarcasm-detector",
    device=-1  # CPU
)
# Load a sentiment analysis pipeline once
_sentiment_pipe = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1
)

def predict_sarcasm(text: str, features: dict) -> float:
    """
    Returns a sarcasm percentage [0.0–100.0].
    Uses text classification + audio feature analysis.
    """
    if not text:
        return 0.0

    # Text-based sarcasm detection
    out = _sarcasm_pipe(text, top_k=1)[0]
    label = out.get("label", "")
    score = out.get("score", 0.0)
    sarcasm_prob = score if label.endswith("1") else 1.0 - score

    # Sentiment analysis
    sentiment = _sentiment_pipe(text, top_k=1)[0]
    sentiment_label = sentiment.get("label", "neutral").lower()

    # Audio feature analysis
    boost = 0.0
    
    # High pitch variation often indicates sarcasm
    pitch = features.get("pitch", 0.0)
    if pitch > 200:  # High pitch
        boost += 0.1
    
    # Low energy with positive words often indicates sarcasm
    energy = features.get("energy", 1.0)
    if energy < 0.02 and any(w in text.lower() for w in ["happy", "great", "awesome", "wonderful"]):
        boost += 0.15
    
    # High zero crossing rate can indicate sarcastic tone
    zcr = features.get("zero_crossing_rate", 0.0)
    if zcr > 0.1:  # High zero crossing rate
        boost += 0.05
    
    # Spectral centroid can indicate voice quality changes
    spectral_centroid = features.get("spectral_centroid", 0.0)
    if spectral_centroid > 3000:  # High spectral centroid
        boost += 0.05

    # Tone-mismatch boost: positive text with unusual audio features
    if sentiment_label == "positive" and (energy < 0.02 or zcr > 0.1):
        boost += 0.1

    final = min(1.0, sarcasm_prob + boost)
    return round(final * 100, 2) 