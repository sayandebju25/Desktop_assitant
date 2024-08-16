import wolframalpha
import pyttsx3
import speech_recognition

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def WolfRamAlpha(query):
    apikey ="P83RQG-RWXLR8VX8R"  # "#paste your api key"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")

def Calc(query):
    Term = str(query)
    Term = Term.replace("jarvis","")
    Term = Term.replace("multiply","*")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("divide","/")
        # Replace additional operators
    Term = Term.replace("modulus", "%")
    Term = Term.replace("and", "&")
    Term = Term.replace("or", "|")
    Term = Term.replace("logical and", "&&")
    Term = Term.replace("logical or", "||")

    # Replace integration, derivative, and limit
    Term = Term.replace("integration", "integrate")
    Term = Term.replace("derivative", "diff")
    Term = Term.replace("limit", "limit")
    

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)

    except:
        speak("The value is not answerable")