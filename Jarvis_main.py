import json
import pyttsx3
import speech_recognition 
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
from camera_functions import open_camera_and_take_photo, close_camera  # Import the functions
# import openai
from config import apikey  # Import API key from config.py
from hugchat import hugchat
# OpenAI API setup
with open("cookies.json", "r") as file:
    cookies = json.load(file)

# Initialize HugChat with cookies
chatbot = hugchat.ChatBot(cookies=cookies)
# openai.api_key = apikey

# def ask_openai(prompt):
#     try:
#         response = openai.Completion.create(
#             model="gpt-4o-mini",
#             prompt=prompt,
#             temperature=0.7,
#             max_tokens=150,
#           top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0
#         )
#         answer = response.choices[0].text.strip()
#         return answer
#     except Exception as e:
#         print(f"Error: {e}")
#         return "Sorry, I couldn't process your request."
def ask_hugchat(prompt):
    try:
        # Generate a response using HugChat
        response = chatbot.chat(prompt)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."
for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()


    if (a==pw):
        print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")    
from INTRO import play_gif
play_gif


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
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
                    speak("Ok sir , You can call me anytime")
                    break 
                # elif "ask" in query:
                #     question = query.replace("ask", "").strip()
                #     answer = ask_openai(question)
                #     speak(answer)
                #     print(answer)

                elif "ask question" in query:
                    while True:
                        speak("What question would you like to ask? Say 'stop' to stop asking questions.")
                        user_question = takeCommand().lower()
                        if "stop" in user_question:
                            speak("Exiting question mode.")
                            break
                        else:
                            response = ask_hugchat(user_question)
                            # Assuming response is a Message object; extract text from it
                            answer = response.text  # Adjust if the attribute name is different
                            lines = answer.split('\n')[:3]
                            formatted_answer = '\n'.join(lines)
                            speak(f"Here's the answer: {formatted_answer}")
                             
                #JARVIS 2.o the Trilogy#################
                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = input("Enter the new password\n")
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done sir")
                    speak(f"Your new password is{new_pw}")
                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i=0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notify.mp3")
                    mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                         )

                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                
                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")

                elif "ipl score" in query:
                   # from plyer import notification  # pip install plyer
                    from plyer import notification  # pip install plyer
                    import requests  # pip install requests
                    from bs4 import BeautifulSoup  # pip install bs4

                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, "html.parser")

                    try:
                        # Find all matches
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
                                # Find team names
                                team_names = match.find_all('div', class_='cb-ovr-flo cb-hmscg-tm-nm')
                                if len(team_names) >= 2:
                                    team1 = team_names[0].get_text().strip()
                                    team2 = team_names[1].get_text().strip()

                                    # Find scores
                                    scores = match.find_all('div', class_='cb-col cb-col-33 cb-tms-scrs')
                                    team1_score = scores[0].get_text().strip() if len(scores) > 0 else "N/A"
                                    team2_score = scores[1].get_text().strip() if len(scores) > 1 else "N/A"

                                    # Print the results
                                    print(f"{team1}: {team1_score}")
                                    print(f"{team2}: {team2_score}")

                                    # Send a notification with the results
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
                     import pyautogui #pip install pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                elif "click my photo" in query:
                    speak("Opening camera, please smile!")
                    open_camera_and_take_photo()
                    close_camera()
                    speak("Photo captured and camera closed.")


   #ADD      

                ########################################

                elif "hello" in query:
                    speak("Hello sir,how are you ?")
                elif "i am fine" in query:
                    speak("that's great,sir")
                elif "how are you" in query:
                    speak("Perfect , sir")   
                
                elif "thank you" in query:
                    speak("you are welcome , sir")   
                
                elif "tired" in query:
                    speak("Playing your favourite songs, sir")
                    a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                    b = random.choice(a)
                    if b==1:
                      webbrowser.open("https://www.youtube.com/watch?v=U10nBuERNIA") #Here put the link of your video)
                    elif b==2:
                        webbrowser.open("https://www.youtube.com/watch?v=fvq6qWP-5tI")
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
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
                elif "youTube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query) 

                elif "news" in query:
                    from NewsRead import latestnews    
                    latestnews()
                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)
                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()

                elif "temperature" in query:    
                    search = "temperature in kolkata"
                    url =f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div",class_="BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "weather" in query:    
                    search = "temperature in kolkata"
                    url =f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div",class_="BNeawe").text
                    speak(f"current{search} is {temp}")    
                
                elif "set an alarm" in query:
                    print("inpt time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a=input("Plese tall the time:- ")
                    alarm(a)
                    speak("Done ,sir")

                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")    
                elif "finally sleep" in query:
                     speak("going to sleep, sir")
                     exit()
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me" + remember.read())
                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break   
                