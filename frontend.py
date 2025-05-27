# import streamlit as st
# import speech_recognition as sr
# import pyttsx3
# import webbrowser
# import datetime
# import os
# import requests

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening...")
#         audio = recognizer.listen(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except:
#         return ""

# def ask_gemini(prompt):
#     api_key = "AIzaSyASo29ZGaQHWjfWnRb5vKjKPCPwuH3rzLc"
#     try:
#         url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
#         headers = {"Content-Type": "application/json"}
#         data = {"contents": [{"parts": [{"text": prompt}]}]}
#         response = requests.post(url, headers=headers, json=data)
#         response_json = response.json()
#         if "candidates" in response_json:
#             return response_json["candidates"][0]["content"]["parts"][0]["text"]
#         else:
#             return "Sorry, I couldn't generate a response."
#     except Exception as e:
#         return f"[Error: {str(e)}]"

# def perform_task(command):
#     if "open google" in command:
#         webbrowser.open("https://www.google.com")
#         return "Opening Google..."
#     elif "time" in command:
#         now = datetime.datetime.now().strftime("%I:%M %p")
#         return f"The time is {now}"
#     elif "play music" in command:
#         music_path = "C:\\Users\\Public\\Music\\Sample Music\\song.mp3"
#         if os.path.exists(music_path):
#             os.startfile(music_path)
#             return "Playing music..."
#         else:
#             return "Music file not found."
#     else:
#         return ask_gemini(command)

# # Streamlit UI
# st.set_page_config(page_title="🎤 Voice Assistant UI", layout="centered")
# st.title("🎤 Voice Assistant")
# st.markdown("Click the button and speak your command into your microphone.")

# if st.button("🎙️ Start Voice Assistant"):
#     command = listen().lower()
#     if command:
#         st.markdown(f"**You said:** `{command}`")
#         result = perform_task(command)
#         st.success(result)
#         speak(result)
#     else:
#         st.warning("No command detected or could not recognize speech.")


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
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

def ask_gemini(prompt):
    api_key = "AIzaSyASo29ZGaQHWjfWnRb5vKjKPCPwuH3rzLc"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"[Error: {str(e)}]"

def perform_task(command):
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}"
    elif "play music" in command:
        music_path = "C:\\Users\\Public\\Music\\Sample Music\\song.mp3"
        if os.path.exists(music_path):
            os.startfile(music_path)
            return "Playing music..."
        else:
            return "Music file not found."
    else:
        return ask_gemini(command)

# Streamlit UI
st.set_page_config(page_title="🎤 Voice Assistant UI", layout="centered")
st.title("🎤 Voice Assistant")
st.markdown("Click 'Start' to activate voice assistant and 'Stop' to finish.")

start = st.button("▶️ Start Voice Assistant")
stop = st.button("⏹️ Stop Voice Assistant")

if start:
    st.session_state["active"] = True

if stop:
    st.session_state["active"] = False

if st.session_state.get("active", False):
    command = listen().lower()
    if command:
        st.markdown(f"**You said:** `{command}`")
        result = perform_task(command)
        st.success(result)
        speak(result)
    else:
        st.warning("No command detected or could not recognize speech.")
