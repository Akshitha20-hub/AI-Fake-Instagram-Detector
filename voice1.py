import streamlit as st
import speech_recognition as sr
import numpy as np
import librosa
import soundfile as sf
import tempfile
from transformers import pipeline

# -------------------------------
# Load Emotion Detection Model
# -------------------------------

emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False
)

# -------------------------------
# Streamlit UI
# -------------------------------

st.title("Real-Time Voice Emotion Recognition")
st.write("Speak through your microphone and the system will detect your emotion.")

# -------------------------------
# Initialize Speech Recognizer
# -------------------------------

recognizer = sr.Recognizer()

# -------------------------------
# Record Audio
# -------------------------------

if st.button("Start Recording"):

    with sr.Microphone() as source:

        st.info("Listening... Please speak")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

        st.success("Recording completed")

        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio.get_wav_data())
            audio_path = temp_audio.name

# -------------------------------
# Speech to Text
# -------------------------------

        try:

            text = recognizer.recognize_google(audio)

            st.subheader("Recognized Speech")
            st.write(text)

        except:
            st.error("Could not understand the audio")
            st.stop()

# -------------------------------
# Audio Feature Extraction
# -------------------------------

        try:

            y, sr_rate = librosa.load(audio_path)

            pitch = np.mean(librosa.yin(y, fmin=50, fmax=300))

            energy = np.mean(librosa.feature.rms(y=y))

            st.subheader("Voice Features")

            st.write("Pitch:", round(pitch,2))
            st.write("Energy:", round(energy,2))

        except:
            st.warning("Audio feature extraction failed")

# -------------------------------
# Emotion Prediction
# -------------------------------

        result = emotion_model(text)

        emotion = result[0]['label']
        score = result[0]['score']

# -------------------------------
# Display Emotion
# -------------------------------

        st.subheader("Detected Emotion")

        st.success(f"Emotion: {emotion}")

        st.write("Confidence Score:", round(score,2))

# -------------------------------
# End
# -------------------------------