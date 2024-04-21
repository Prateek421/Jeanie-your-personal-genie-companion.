import pyttsx3
import speech_recognition as sr
import eel
import time
from flask import Flask, render_template, request
import subprocess
#from engine.face import implementation

app = Flask(__name__)
@eel.expose
def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174) 
    #print(voices)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
@eel.expose
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage('Listening....')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, 10, 6)
    try:
        print("Recognizing...")
        eel.DisplayMessage('Recognizing...')
        query=r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        #speak(var)
        
    except Exception as e:
        return ""
    return query.lower()




@eel.expose
def allCommands(message=1):
    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)
    try:
        
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what do you want to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
    eel.ShowHood()
if __name__ == '__main__':
    app.run(debug=True)