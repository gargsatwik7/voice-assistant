import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎙️ Listening... Please speak now."):
            audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

def ask_gemini(prompt):
    api_key = "YOUR_API_KEY"  # 🔐 Replace this with your Gemini API key
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "❌ Sorry, I couldn't generate a response."
    except Exception as e:
        return f"❌ [Error: {str(e)}]"

def perform_task(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "🌐 Opening Google..."
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"🕒 The time is {now}"
    elif "play music" in command:
        music_path = "C:\\Users\\Public\\Music\\Sample Music\\song.mp3"
        if os.path.exists(music_path):
            os.startfile(music_path)
            return "🎵 Playing music..."
        else:
            return "⚠️ Music file not found."
    else:
        return ask_gemini(command)

# Streamlit UI
st.set_page_config(page_title="🎤 Smart Voice Assistant", layout="centered")
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 700;
            text-align: center;
            color: #4CAF50;
            margin-top: 20px;
        }
        .section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 14px;
            color: #999999;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎙️ Smart Voice Assistant</div>", unsafe_allow_html=True)
st.markdown("Speak commands like **'open Google'**, **'what is the time'**, or ask anything using Gemini AI.")

# Session state
if "active" not in st.session_state:
    st.session_state.active = False

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("▶️ Start Listening"):
        st.session_state.active = True
with col2:
    if st.button("⏹️ Stop"):
        st.session_state.active = False
        st.success("✅ Voice assistant stopped.")

# Active session block
if st.session_state.active:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.info("🎧 Waiting for your voice input...")
    command = listen().lower()
    if command:
        st.markdown(f"🗣️ **You said:** `{command}`")
        result = perform_task(command)
        st.success(result)
        speak(result)
    else:
        st.warning("😕 Could not recognize your speech. Try again.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ using Streamlit, Gemini API, and Speech Recognition</div>", unsafe_allow_html=True)
