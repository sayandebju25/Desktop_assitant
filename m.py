import pyttsx3
import speech_recognition as sr
import requests
import datetime
import os
import pyautogui
import random
import webbrowser
import speedtest
from bs4 import BeautifulSoup
from plyer import notification
from pygame import mixer
from camera_functions import open_camera_and_take_photo, close_camera
import openai
from config import apikey  # Make sure to add your API key in a config file

# OpenAI API setup
openai.api_key = apikey

def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."

# Load password
for i in range(3):
    a = input("Enter Password to open Jarvis: ")
    with open("password.txt", "r") as pw_file:
        pw = pw_file.read().strip()

    if a == pw:
        print("WELCOME SIR! PLEASE SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif i == 2 and a != pw:
        exit()
    elif a != pw:
        print("Try Again")

from INTRO import play_gif
play_gif

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def alarm(query):
    with open("Alarmtext.txt", "a") as timehere:
        timehere.write(query)
    os.startfile("alarm.py")

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir, you can call me anytime")
                    break
                
                # JARVIS 2.0 - The Trilogy
                elif "change password" in query:
                    speak("What's the new password?")
                    new_pw = input("Enter the new password: ")
                    with open("password.txt", "w") as new_password:
                        new_password.write(new_pw)
                    speak(f"Your new password is {new_pw}")

                elif "schedule my day" in query:
                    tasks = []
                    speak("Do you want to clear old tasks (Please speak YES or NO)?")
                    query = takeCommand().lower()
                    if "yes" in query:
                        with open("tasks.txt", "w") as file:
                            file.write("")
                        no_tasks = int(input("Enter the number of tasks: "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task: "))
                            with open("tasks.txt", "a") as file:
                                file.write(f"{i}. {tasks[i]}\n")
                    elif "no" in query:
                        no_tasks = int(input("Enter the number of tasks: "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task: "))
                            with open("tasks.txt", "a") as file:
                                file.write(f"{i}. {tasks[i]}\n")

                elif "show my schedule" in query:
                    with open("tasks.txt", "r") as file:
                        content = file.read()
                    mixer.init()
                    mixer.music.load("notify.mp3")
                    mixer.music.play()
                    notification.notify(
                        title="My Schedule:",
                        message=content,
                        timeout=15
                    )

                elif "open" in query:
                    query = query.replace("open", "").replace("jarvis", "")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                
                elif "internet speed" in query:
                    wifi = speedtest.Speedtest()
                    upload_net = wifi.upload() / 1048576
                    download_net = wifi.download() / 1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi Download Speed is", download_net)
                    speak(f"Wifi Download Speed is {download_net:.2f} MBps")
                    speak(f"Wifi Upload Speed is {upload_net:.2f} MBps")

                elif "ipl score" in query:
                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, "html.parser")

                    try:
                        matches = soup.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')

                        if not matches:
                            print("No matches found.")
                            notification.notify(
                                title="Cricket Scores",
                                message="No matches are currently being played.",
                                timeout=15
                            )
                        else:
                            for match in matches:
                                team_names = match.find_all('div', class_='cb-ovr-flo cb-hmscg-tm-nm')
                                if len(team_names) >= 2:
                                    team1 = team_names[0].get_text().strip()
                                    team2 = team_names[1].get_text().strip()

                                    scores = match.find_all('div', class_='cb-col cb-col-33 cb-tms-scrs')
                                    team1_score = scores[0].get_text().strip() if len(scores) > 0 else "N/A"
                                    team2_score = scores[1].get_text().strip() if len(scores) > 1 else "N/A"

                                    print(f"{team1}: {team1_score}")
                                    print(f"{team2}: {team2_score}")

                                    notification.notify(
                                        title="Cricket Score",
                                        message=f"{team1}: {team1_score}\n{team2}: {team2_score}",
                                        timeout=15
                                    )
                                else:
                                    print("Could not find team names for a match.")

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        notification.notify(
                            title="Cricket Scores",
                            message="An error occurred while fetching the scores.",
                            timeout=15
                        )

                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                    im = pyautogui.screenshot()
                    im.save("ss.jpg")

                elif "click my photo" in query:
                    speak("Opening camera, please smile!")
                    open_camera_and_take_photo()
                    close_camera()
                    speak("Photo captured and camera closed.")

                elif "hello" in query:
                    speak("Hello sir, how are you?")

                elif "i am fine" in query:
                    speak("That's great, sir")

                elif "how are you" in query:
                    speak("Perfect, sir")

                elif "thank you" in query:
                    speak("You are welcome, sir")

                elif "tired" in query:
                    speak("Playing your favorite songs, sir")
                    a = [1, 2, 3]
                    b = random.choice(a)
                    if b == 1:
                        webbrowser.open("https://www.youtube.com/watch?v=U10nBuERNIA")
                    elif b == 2:
                        webbrowser.open("https://www.youtube.com/watch?v=fvq6qWP-5tI")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("Video paused")

                elif "play" in query:
                    pyautogui.press("k")
                    speak("Video played")

                elif "mute" in query:
                    pyautogui.press("m")
                    speak("Video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up, sir")
                    volumeup()

                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()

                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)

                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)

                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)

                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)

                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()

                elif "calculate" in query:
                    from Calculatenumbers import Calc
                    query = query.replace("calculate", "").replace("jarvis", "")
                    Calc(query)

                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()

                elif "temperature" in query or "weather" in query:
                    search = "temperature in kolkata"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"Current {search} is {temp}")

                elif "set an alarm" in query:
                    speak("Set the time")
                    a = input("Please tell the time (example: 10 10 10): ")
                    alarm(a)
                    speak("Done, sir")

                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(f"Sir, the time is {strTime}")

                elif "finally sleep" in query:
                    speak("Going to sleep, sir")
                    exit()

                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").replace("jarvis", "")
                    speak(f"You told me: {rememberMessage}")
                    with open("Remember.txt", "a") as remember:
                        remember.write(rememberMessage + "\n")

                elif "what do you remember" in query:
                    with open("Remember.txt", "r") as remember:
                        speak("You told me: " + remember.read())

                elif "shutdown the system" in query:
                    speak("Are you sure you want to shutdown?")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no): ")
                    if shutdown.lower() == "yes":
                        os.system("shutdown /s /t 1")
                    elif shutdown.lower() == "no":
                        break
                
                else:
                    # Use OpenAI API to answer the question
                    response = ask_openai(query)
                    speak(response)
