

📄 README.md

# Audio to Text Transcription App 🎙️📝

This web app allows you to easily transcribe audio files in Arabic and English using two powerful transcription engines:

- **Whisper (Local model by OpenAI)** — Higher accuracy, runs entirely offline.
- **Google Web Speech API** — Fast and efficient, requires an internet connection.

You can upload audio files (`.m4a`, `.wav`, `.mp3`), transcribe them, edit the extracted text, download the text file, and even export a timed subtitle file (`.srt`).

You can access the app through: [https://zaidaudiototext.streamlit.app/](https://zaidaudiototext.streamlit.app/)
---

## 🔥 Features
- Upload audio files (supports `.m4a`, `.wav`, `.mp3`).
- Choose transcription engine: Whisper (local) or Google Web Speech.
- For Whisper:
  - Select performance priority: `Fast`, `Balanced`, or `Accurate`.
- See estimated transcription time based on file length.
- Live progress bar during transcription.
- Edit the extracted text directly in the app.
- Download the final transcription as a `.txt` or `.srt` subtitle file.
- Audio preview inside the app.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/audio-to-text-app.git
   cd audio-to-text-app
   ```

2.	Install dependencies:

```pip install -r requirements.txt```


3.	Make sure you have ffmpeg installed:
On MacOS:

```brew install ffmpeg```

On Windows (choco required):

```choco install ffmpeg```


	4.	Run the Streamlit app:

```streamlit run app.py```
⸻

🛠️ Requirements
	•	Python 3.8+
	•	Streamlit
	•	Whisper
	•	SpeechRecognition
	•	pydub
	•	torch
	•	ffmpeg (system installed)

⸻

📬 About the Developer

Developed by: Zaid Altukhi
Passionate about AI, data science, and building intelligent applications. 🚀
📧 zaid@altukhizm.com

⸻

✨ Future Improvements
	•	Auto-language detection for multilingual audios.
	•	Speaker diarization (separate different speakers).
	•	Upload longer files with memory optimization.
	•	More customizable subtitle formatting options.

⸻
