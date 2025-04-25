import streamlit as st
import os
import speech_recognition as sr
from pydub import AudioSegment
import re


st.set_page_config(
    page_title= 'Audio to Text Transcription App',
    page_icon=' 🎙️ ',
    layout="wide",
    base='light')

# Title of the app
st.title("Audio to Text Transcription App")

st.sidebar.title("About This App")
st.sidebar.markdown("""
**Audio to Text Transcription App**  
Easily transcribe audio files (Arabic/English) using powerful engines (Whisper or Google API).

**Developed by: Zaid Altukhi**  
Passionate about AI, data science, and building intelligent applications. 🚀
[zaid@altukhizm.com](mailto:zaid@altukhizm.com)
""")
st.sidebar.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload your audio file (m4a, wav, mp3)", type=["m4a", "wav", "mp3"])

language = st.selectbox(
    "Select transcription language:",
    options=["Arabic (ar-SA)", "English (en-US)"]
)
lang_code = "ar-SA" if language == "Arabic (ar-SA)" else "en-US"

engine = st.selectbox(
    "Select transcription engine:",
    options=["Google Web Speech API"]
)

st.sidebar.info("Note: Google Web Speech API is faster but requires an internet connection.")

if uploaded_file is not None:
    st.sidebar.audio(uploaded_file, format="audio/m4a")

    if st.sidebar.button("Start Transcription"):
        # Placeholders for messages
        info_message = st.empty()
        success_message = st.empty()
        progress_bar = st.empty()

        # Save the uploaded file
        input_audio_path = "input_audio.m4a"
        with open(input_audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert to WAV if necessary
        output_audio_path = "converted_audio.wav"
        info_message.info("Converting audio file to WAV format...")
        audio = AudioSegment.from_file(input_audio_path)
        audio.export(output_audio_path, format="wav")
        success_message.success("Conversion done ✅")

        duration_seconds = len(audio) / 1000  # duration in seconds
        expected_time_minutes = round(duration_seconds / 60 * 2.5)
        st.markdown(f"🕒 **Estimated transcription time:** ~{expected_time_minutes} minutes", unsafe_allow_html=True)
        st.caption("⏳ Note: Actual time may vary depending on your device performance and file size.")

        progress_bar.progress(0)

        info_message.info("Using Google Web Speech API...")
        recognizer = sr.Recognizer()
        with sr.AudioFile(output_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=lang_code)

        progress_bar.progress(100)
        success_message.success("Transcription complete!")

        edited_text = st.text_area("Edit the extracted text:", text, height=400)
        st.download_button("Download Edited Text", edited_text, file_name="transcription.txt")
        st.success("✅ The transcribed text is ready for editing and download.")

        # Clear all placeholders after transcription is displayed
        info_message.empty()
        success_message.empty()
        progress_bar.empty()
