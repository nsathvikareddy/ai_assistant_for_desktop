import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import random
import numpy as np
import psutil # type: ignore
import re
from plyer import notification


with open("intents.json") as file:
    data = json.load(file)

model = load_model("my_model.keras")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening..........", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing..........", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week    
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Gagana, it's {day} and the time is {t}")
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Gagana, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Gagana, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()  
    speak("Hey Gagana, today's schedule is")
    week = {
        "monday": "Gagana from 8:30 am to 9:30 am you have advanced iot class, from 9:30 am to 10:20 am you have cloud computing class, from 10:20 am to 10:40 am you have short break, from 10:40 am to 11:30 am you have indian knowledge system class, from 11:30 am to 12:30 pm you have lunch break, from 12:30 to 2:30 you have advanced iot lab",
        "tuesday": "Gagana from 8:30 am to 10:20 am you have information and network security lab, from 10:20 am to 10:40 am you have short break, from 10:40 to 11:30 you have Sustainable solar energy technology and job opportunity class, from 12:30 pm to 1:20 pm you have lunch break, from 1:20 to 3:20 you have bizotic training, from 3:20 to 4:30 you have information and network security class",
        "wednesday": "Gagana from 8:30 am to 9:25 am you have information and network security class, from 9:30 am to 10:20 am you have cloud computing class, from 10:20 am to 10:40 am you have short break, from 10:40 am to 12:30 pm you have natural language processing class, from 12:30 pm to 1:20 pm you have lunch break, from 1:20 to 3:20 you have bizotic training, from 3:20 pm to 4:30 pm you have advanced iot class",
        "thursday": "Gagana from 8:30 am to 10:20 am you have computer vision and application class, from 10:20 am to 10:40 am you have short break, from 10:40 am to 12:30 pm you have Sustainable solar energy technology and job opportunity class, from 12:30 pm to 1:20 pm you have lunch break, from 1:20 pm to 2:20 pm you have advanced iot class",
        "friday": "Gagana from 8:30 am to 9:25 am you have cloud computing class, from 9:30 am to 10:20 am you have information and network security class, from 10:20 am to 10:40 am you have short break, from 10:40 am to 12:30 pm you have cloud computing lab, from 12:30 pm to 1:20 pm you have lunch break, from 1:20 pm to 2:20 pm you have computer vision and application class, from 2:20 pm to 3:20 pm you have natural language processing class",
        "saturday": "Gagana it is your free day but still it is better to work on projects or update your resume or work on github repository",
        "sunday": "Gagana it's a chill day just have fun and enjoy with your family",
    }
    if day in week.keys():
        speak(week[day])
    else:
        speak("Sorry, I could not find today's schedule.")

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(command):  
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("Gagana, what should i search on google")
        s = command().lower()
        webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #    speak("opening your microsoft edge")
    #    os.startfile()

def set_reminder(query=None):
    if not query:
        speak("What should I remind you about?")
        query = command().lower()

    now = datetime.datetime.now()

    match = re.search(r"(\d{1,2}):(\d{2})", query)
    date_set = False

    if "today" in query:
        reminder_time = now.replace(hour=int(match.group(1)), minute=int(match.group(2)), second=0)
        date_set = True
    elif "tomorrow" in query:
        reminder_time = now.replace(day=now.day + 1, hour=int(match.group(1)), minute=int(match.group(2)), second=0)
        date_set = True

    if not date_set:  # Ask for date and time if not mentioned
        speak("Please tell me the date (YYYY-MM-DD).")
        date_str = command()

        speak("Please tell me the time (HH:MM).")
        time_str = command()

        try:
            reminder_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            reminder_time = reminder_date.replace(
                hour=int(time_str.split(":")[0]), minute=int(time_str.split(":")[1]), second=0
            )
        except ValueError:
            speak("Invalid date or time format. Please try again.")
            return

    speak(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Wait until the reminder time
    while datetime.datetime.now() < reminder_time:
        time.sleep(1)
    
    speak("Time's up! Here is your reminder: {reminder_text}")

    
def play_music(query):
    if 'play music' in query:
        speak("Gagana, which song should I play?")
        song = command().lower()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

def alarm(query):
    if "set alarm" in query:
        match = re.search(r"(\d+)\s*(minute|minutes|second|seconds)", query)
        if match:
            time_value = int(match.group(1))
            time_unit = match.group(2)

            if "second" in time_unit:
                seconds = time_value
            else:
                seconds = time_value * 60  # Convert minutes to seconds

            speak(f"Setting an alarm for {time_value} {time_unit}.")
            time.sleep(seconds)
            speak("Time's up!")

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Gagana our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Gagana we have sufficient battery to continue to work on the project")
    elif percentage>=40 and percentage<=75:
        speak("Gagana please start charging the system")
    else:
        speak("Gagana there is very low battery charge the system as soon as possible")    

if __name__ == "__main__":
    speak("Hello I am Saanvi, your AI assistant")
    wishMe()
    while True:
        query = command().lower()
        # query = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")    # type: ignore
            speak("volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")    # type: ignore
            speak("volume decreased")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")    # type: ignore
            speak("volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif 'play music' in query:
            play_music(query)
        elif 'set alarm' in query:
            alarm(query)
        elif "set a reminder" in query:
            set_reminder()
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()

# speak("Hello, I am Saanvi")
