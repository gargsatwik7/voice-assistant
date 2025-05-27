import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import json
import requests

# ✅ Configure Gemini API client
api_key="AIzaSyASo29ZGaQHWjfWnRb5vKjKPCPwuH3rzLc"  # Replace with your key

# ✅ Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        speak("Sorry, I didn't get that.")
        return ""

def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Sorry, I couldn't generate a response."
            
    except Exception as e:
        return f"An error occurred: {str(e)}"

def perform_task(command):
    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "play music" in command:
        music_path = "C:\\Users\\Public\\Music\\Sample Music\\song.mp3"
        if os.path.exists(music_path):
            os.startfile(music_path)
        else:
            speak("Music file not found.")

    else:
        answer = ask_gemini(command)
        speak(answer)

def main():
    speak("Hi, I'm your smart assistant. How can I help?")
    while True:
        command = listen().lower()
        if command:
            if "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            perform_task(command)

if __name__ == "__main__":
    main()