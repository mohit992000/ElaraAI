import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import threading
import time
from datetime import datetime as dt

# Function to make Elara speak
def speak_response(response):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Slow down speech to 150 words per minute
    engine.say(response)
    engine.runAndWait()

# Function to listen for commands
def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak_response("I'm listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak_response("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            speak_response("There seems to be an issue with the voice recognition service.")
            return None

# Function to fetch news
def get_news():
    API_KEY = '77ac4f7a7b8748dfb5747cf66b92649b'  # NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            headlines = [article["title"] for article in news_data["articles"][:5]]
            return "Here are the top news headlines: " + " | ".join(headlines)
        else:
            return "Sorry, I couldn't fetch the news at the moment."
    except Exception as e:
        return f"There was an error retrieving the news: {e}"

# Function to fetch weather data using Meteomatics API
def get_weather():
    USERNAME = "self_kumar_mohit"  # Meteomatics username
    PASSWORD = "Wt9N40sM3k"        # Meteomatics password

    base_url = "https://api.meteomatics.com"
    date_time = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # Current UTC time
    parameter = "t_2m:C"  # Temperature at 2 meters in Celsius
    latitude = "52.520551"  # Example: Berlin's latitude
    longitude = "13.461804"  # Example: Berlin's longitude
    output_format = "json"

    url = f"{base_url}/{date_time}/{parameter}/{latitude},{longitude}/{output_format}"

    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD))
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data["data"]["t_2m:C"][0]["value"]
            return f"The current temperature at {latitude}, {longitude} is {temperature}°C."
        else:
            return f"Unable to fetch weather data. Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"There was an error connecting to the weather service: {e}"

# Function to set a reminder
def set_reminder(reminder, seconds):
    def reminder_thread():
        time.sleep(seconds)
        speak_response(f"Reminder: {reminder}")
        print(f"Reminder: {reminder}")
    thread = threading.Thread(target=reminder_thread)
    thread.start()

# Function to handle commands
def handle_command(command):
    if 'time' in command:
        response = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    elif 'date' in command:
        response = f"Today's date is {datetime.date.today()}."
    elif 'open google' in command:
        response = "Opening Google for you."
        webbrowser.open("https://www.google.com")
    elif 'search for' in command:
        query = command.replace("search for", "").strip()
        response = f"Searching for {query} on the web."
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif 'news' in command:
        response = get_news()
    elif 'weather' in command:
        response = get_weather()
    elif 'remind me to' in command:
        reminder = command.replace("remind me to", "").strip()
        response = f"What time should I remind you about {reminder}?"
        speak_response(response)
        reminder_time = listen_to_command()
        if reminder_time and "in" in reminder_time:
            try:
                seconds = int(reminder_time.split()[1]) * 60
                set_reminder(reminder, seconds)
                response = f"Reminder set for {seconds // 60} minutes."
            except ValueError:
                response = "Sorry, I couldn't understand the time for the reminder."
        else:
            response = "Sorry, I couldn't understand the time for the reminder."
    elif "exit" in command:
        response = "Goodbye! Have a nice day."
        speak_response(response)
        return "exit"
    else:
        response = "I didn't understand that. Can you please repeat?"
    speak_response(response)
    return None

# Main function to run Elara
def main():
    speak_response('Hello, I am Elara, your personal assistant. How can I help you today?')
    while True:
        command = listen_to_command()
        if command:
            if handle_command(command) == "exit":
                break

# Ensure the program runs
if __name__ == "__main__":
    main()



    