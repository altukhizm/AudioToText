import streamlit as st
import os
import speech_recognition as sr
from pydub import AudioSegment
import whisper
import re

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
uploaded_file = st.sidebar.file_uploader("Upload your audio file (m4a, wav, mp3)", type=["m4a", "wav", "mp3"])

language = st.sidebar.selectbox(
    "Select transcription language:",
    options=["Arabic (ar-SA)", "English (en-US)"]
)
lang_code = "ar-SA" if language == "Arabic (ar-SA)" else "en-US"

engine = st.sidebar.selectbox(
    "Select transcription engine:",
    options=["Whisper (local)", "Google Web Speech API"]
)

# Add performance priority option for Whisper
priority = None
if engine == "Whisper (local)":
    priority = st.sidebar.selectbox(
        "Select performance priority:",
        options=["Fast (small model)", "Balanced (medium model)", "Accurate (large model)"]
    )

st.sidebar.info("Note: Whisper is more accurate but slower. Google is faster but requires an internet connection.")

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

        if engine == "Whisper (local)":
            info_message.info("Loading Whisper model...")
            # Select model size based on priority
            if priority == "Fast (small model)":
                model = whisper.load_model("small")
            elif priority == "Accurate (large model)":
                model = whisper.load_model("large")
            else:
                model = whisper.load_model("medium")
            progress_bar.progress(20)
            success_message.success("Model loaded successfully ✅")
            info_message.info("Transcribing audio...")
            progress_bar.progress(50)
            result = model.transcribe(output_audio_path, language=lang_code.split('-')[0])
            text = result["text"]
            progress_bar.progress(100)

            def seconds_to_srt_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                millis = int((seconds - int(seconds)) * 1000)
                return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

            srt_content = ""
            srt_index = 1
            for segment in result['segments']:
                start = seconds_to_srt_time(segment['start'])
                end = seconds_to_srt_time(segment['end'])
                text_seg = segment['text'].strip()
                # Split text into sentences using punctuation
                sentences = re.split(r'(?<=[.!?]) +', text_seg)
                segment_duration = (segment['end'] - segment['start']) / max(len(sentences), 1)
                for i, sentence in enumerate(sentences):
                    seg_start = seconds_to_srt_time(segment['start'] + i * segment_duration)
                    seg_end = seconds_to_srt_time(segment['start'] + (i + 1) * segment_duration)
                    srt_content += f"{srt_index}\n{seg_start} --> {seg_end}\n{sentence.strip()}\n\n"
                    srt_index += 1

            st.download_button("Download SRT File", srt_content, file_name="transcription.srt")
            st.subheader("Preview SRT Content:")
            st.text_area("SRT Preview", srt_content, height=300)

        else:
            info_message.info("Using Google Web Speech API...")
            recognizer = sr.Recognizer()
            with sr.AudioFile(output_audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=lang_code)

        success_message.success("Transcription complete!")

        edited_text = st.text_area("Edit the extracted text:", text, height=400)
        st.download_button("Download Edited Text", edited_text, file_name="transcription.txt")
        st.success("✅ The transcribed text is ready for editing and download.")

        # Clear all placeholders after transcription is displayed
        info_message.empty()
        success_message.empty()
        progress_bar.empty()