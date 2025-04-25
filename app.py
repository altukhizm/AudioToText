import streamlit as st
import os
import speech_recognition as sr
import tempfile

st.set_page_config(
    page_title='Audio to Text Transcription App',
    page_icon='🎙️',
    layout="wide",
)

# Title of the app
st.image("Audio Convert Icon.png", width=100)
st.title("Audio to Text Transcription App")

st.sidebar.title("About This App")
st.sidebar.markdown("""
**Audio to Text Transcription App**  
Easily transcribe audio files (Arabic/English) using Google Web Speech API.

**Developed by: Zaid Altukhi**  
Passionate about AI, data science, and building intelligent applications. 🚀
[zaid@altukhizm.com](mailto:zaid@altukhizm.com)
""")
st.sidebar.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload your audio file (wav only preferred)", type=["wav", "mp3", "m4a"])

language = st.selectbox(
    "Select transcription language:",
    options=["Arabic (ar-SA)", "English (en-US)"]
)
lang_code = "ar-SA" if language == "Arabic (ar-SA)" else "en-US"

st.markdown("🔎 **Transcription Engine:** Google Web Speech API (Auto-selected)")
st.sidebar.info("Note: Google Web Speech API is faster but requires an internet connection.")

if uploaded_file is not None:
    st.sidebar.audio(uploaded_file)

    if st.button("Start Transcription"):
        # Placeholders
        info_message = st.empty()
        success_message = st.empty()
        progress_bar = st.empty()

        info_message.info("Preparing file for transcription...")
        
        # Save uploaded file as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(uploaded_file.read())
            temp_audio_path = temp_audio_file.name

        success_message.success("Audio file ready ✅")

        # Estimate transcription time (assume simple estimation)
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            duration_seconds = source.DURATION
        expected_time_minutes = round(duration_seconds / 60 * 2.5)
        
        st.markdown(f"🕒 **Estimated transcription time:** ~{expected_time_minutes} minutes", unsafe_allow_html=True)
        st.caption("⏳ Note: Actual time may vary depending on your device performance and file size.")

        progress_bar.progress(20)
        info_message.info("Starting transcription...")

        try:
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=lang_code)

            progress_bar.progress(100)
            success_message.success("Transcription complete!")

            edited_text = st.text_area("Edit the extracted text:", text, height=400)
            st.download_button("Download Edited Text", edited_text, file_name="transcription.txt")
            st.success("✅ The transcribed text is ready for editing and download.")
        
        except Exception as e:
            st.error(f"❌ Error during transcription: {str(e)}")

        # Cleanup
        info_message.empty()
        success_message.empty()
        progress_bar.empty()

        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
