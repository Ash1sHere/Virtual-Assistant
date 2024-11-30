import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import requests

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the first voice
engine.setProperty('rate', 175)  # Set speaking rate

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you today?")

def listen():
    """Listen for user commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that. Could you repeat?")
            return None
        except sr.RequestError:
            speak("There seems to be a problem with the internet connection.")
            return None

def get_weather(city):
    """Fetch weather data for a given city."""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The current weather in {city} is {weather} with a temperature of {temp} degrees Celsius."
        else:
            return "I couldn't fetch the weather data. Please check the city name."
    except requests.exceptions.RequestException:
        return "Unable to connect to the weather service."

def execute_command(command):
    """Execute the user's command."""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "weather" in command:
        speak("Which city should I check the weather for?")
        city = listen()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
    elif "open file" in command:
        speak("Which file would you like to open?")
        file_path = listen()
        if file_path:
            try:
                os.system(f"open {file_path}")
                speak("File opened successfully.")
            except Exception:
                speak("I couldn't open the file. Please check the path.")
    elif "quit" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I can perform basic tasks like telling the time, opening websites, or checking the weather.")

if __name__ == "__main__":
    greet_user()
    while True:
        user_command = listen()
        if user_command:
            execute_command(user_command)