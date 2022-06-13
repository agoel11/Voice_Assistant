# Please make sure that th# Please make sure that the folder with this code has the User in the path
# We did not do our own art
# Link to the image with the face is here: https://www.freepik.com/premium-vector/abstract-wireframe-digital-human-face-ai-artificial-intelligence-concept_5651035.htm
import time
from datetime import date
import speech_recognition as sr
import pyttsx3 as speak
import requests
import webbrowser
import subprocess
import pickle
from time import sleep
import os
import tkinter as tk
from tkinter import * 
from PIL import ImageTk, Image

LARGE_FONT= ("Verdana", 12)

nothing_key = 'afljkdasjkldafkj'

default = {'rate': 130, 'volume': 0.75, 'voice': 1}

positive = ["good", "well", "great", "awesome", "wonderful", "nice"]

global timer_alarm_check
timer_alarm_check = 0

path = os.path.dirname(__file__)

user = path.split('\\')
user = user[2]


print(user)
with open(path + '\\preferences.pickle', 'rb') as f:
    unpickler = pickle.Unpickler(f)
    preferences = unpickler.load()



#makes the program talk
def talk(talk):
    sound = speak.init()
    voices = sound.getProperty('voices')
    volume = sound.getProperty('volume')
    rate = sound.getProperty('rate')
    sound.setProperty('voice', voices[preferences['voice']].id)   
    sound.setProperty('rate', preferences['rate'])
    sound.setProperty('volume', preferences['volume'])
    sound.say(talk)
    sound.runAndWait()
    sound.stop()
    
def talk_preferences(rate, volume, voice):
    global preferences
    preferences = {'rate': rate, 'volume': volume, 'voice': voice}
    with open(path + '//preferences.pickle', 'wb') as f:
        pickle.dump(preferences, f, protocol=pickle.HIGHEST_PROTOCOL)


#makes the program listen
def listen():
    global say
    say = 'talk'
    print(say)
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
        except:
            voice_data = nothing_key
        global command
        command = voice_data
        
    
def who():
    talk("I am Primo, your personal voice assistant")
    

def hay():
    talk("I am good, how are you?")
    listen()
    good = False
    for x in positive:
        if x in command:
            if 'no' in command or 'not' in command:
                good = False
            else:
                good = True
    if good:
        talk('Great')
    else:
        talk("Sorry to hear that.")


def search():
    talk("What do you want to search for")
    listen()
    if nothing_key in command:
        talk('I am sorry, I did not catch that. Please try again.')
        listen()
    search = command
    if nothing_key in search:
        talk('I am sorry, I still cannot hear you')
    else:
        webbrowser.open('https://google.com/search?q=' + search)
        talk("Here is what I found for" + search)


def covid_counter():
    webbrowser.open('https://www.worldometers.info/coronavirus/')
    talk('Here is a live coronavirus tracker')
    
def news():
    webbrowser.open('https://news.google.com')
    talk('Here is the news')

def place_search():
    talk('Where do you want to search?')
    listen()
    if nothing_key in command:
        talk('I am sorry, I did not catch that. Please try again.')
        listen()
    search = command
    if nothing_key in search:
        talk('I am sorry, I still cannot hear you')
    else:
        webbrowser.open('https://www.google.com/maps/place/{}'.format(search))
        talk('Here is what I found for' + command)

def play():
    talk("What do you want to play")
    listen()
    if nothing_key in command:
        talk('I am sorry, I did not catch that. Please try again.')
        listen()
    search = command
    if nothing_key in search:
        talk('I am sorry, I still cannot hear you')
    else:
        webbrowser.open('https://www.youtube.com/results?search_query=' + command)
        talk("Here is what I found for" + command)


def dates():
    today = date.today()
    talk(today)


def times():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    talk(current_time)

def note():
    subprocess.call("C:/Windows/notepad.exe")

def calculator():
    subprocess.call("C:/Windows/System32/calc.exe")

def weather():
    api_key = "0fb23c99f9151f5184396d18c44225fb"
    talk('What city are you in?')
    listen()
    if nothing_key in command:
        talk('I am sorry, I did not catch that. Please try again.')
        listen()
    city = command
    if nothing_key in city:
        talk('I am sorry, I still cannot hear you')
    else:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        cityname = city
        complete_url = base_url + "appid=" + api_key + "&q=" + cityname
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":

            y = x["main"]
            currenttemp = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]

            temp = (str(round((1.8 * (currenttemp - 272.15) + 32) - 2))+ " degrees fahrenheit")
            d = str(weather_description)
            talk("The temperature in {} is currently {} with {}".format(city, temp, d))
        else:
            talk('I am sorry, I failed to get the weather for {}'.format)

def rate(speed):
    if speed == True:
        preferences['rate'] += 20
        if preferences['rate'] >= 300:
            preferences['rate'] = 300
    if speed == False:
        preferences['rate'] = preferences['rate'] - 20
        if preferences['rate'] <= 20:
            preferences['rate'] = 20
    talk_preferences(rate = preferences['rate'], volume = preferences['volume'], voice = preferences['voice'])
        
def volume(volume):
    if volume == True:
        preferences['volume'] += 0.2
        if preferences['volume'] >= 1:
            preferences['volume'] = 1
    if volume == False:
        preferences['volume'] -= 0.2
        if preferences['volume'] <= 0.1:
            preferences['volume'] = 0.1
    talk_preferences(rate = preferences['rate'], volume = preferences['volume'], voice = preferences['voice'])
    
def change_voice(voice):
    if voice == 1:
        talk_preferences(rate = preferences['rate'], volume = preferences['volume'], voice = 0)
    else:
        talk_preferences(rate = preferences['rate'], volume = preferences['volume'], voice = 1)
    listen()
    if "yes" in command:
        talk('okay')
    if 'no' in command:
        if preferences['voice'] == 1:
            talk_preferences(preferences['rate'], preferences['volume'], 0)
        else:
            talk_preferences(preferences['rate'], preferences['volume'], 1)
            
def settings():
    talk("what setting would you like to change")
    sleep(0.2)
    talk("you may choose rate volume or sound. You may also say defaults to reset to defaults")
    listen()
    if nothing_key in command:
        talk('I cannot hear you, please try again.')
        listen()
    if nothing_key not in command:
        if 'rate' in command:
            talk('faster or slower?')
            listen()
            if 'faster' in command:
                rate(True)
            else:
                rate(False)
            talk('rate changed')
        elif 'volume' in command:
            talk('louder or softer?')
            listen()
            if 'louder' in command:
                volume(True)
            else:
                volume(False)
            talk('volume changed')
        elif 'sound' in command:
            change_voice(preferences['voice'])
            print(preferences)
        if 'default' in command:
            talk_preferences(default['rate'], default['volume'], default['voice'])
            talk('Settings Reset')
    else:
        talk('I am sorry, I still cannot hear you')

def mail():
    webbrowser.open('https://mail.google.com')
    talk('Here is your mail.')
        
def dictate():
    talk('What would you like to call the document? Keep in mind that if you name it an existing document, it will be overwritten. Say end dictate to end dictation.')
    listen()
    name = command
    talk('Say what you would like for it to say.')
    with open('C:\\Users\\{}\\Documents\\{}.txt'.format(user, name), 'wt') as f:
        listen()
        f.write(command)
        listen()
        while 'end dictate' not in command:
            f.write(command)
            listen()
        
        f.close()
    os.startfile('C:\\Users\\{}\\Documents\\{}.txt'.format(user, name))



# File Explorer
def file():
    talk('Do you want to open documents, desktop, or downloads?')
    listen()
    if nothing_key in command:
        talk('I am sorry I could not hear you. Please try again')
        listen()
    
    if nothing_key not in command:
        
        if 'desktop' in command:
            subprocess.Popen('explorer C:\\Users\\{}\\Desktop'.format(user))
        if 'document' in command:
            subprocess.Popen('explorer C:\\Users\\{}\\Documents'.format(user))
        if 'downloads' in command:
            subprocess.Popen('explorer C:\\Users\\{}\\Dowloads'.format(user))
    else:
        talk('I am sorry, I still cannot hear you')
    
        

                
def interpret():
    if  "how are you" in command:
        hay()


    if "who are you" in command:
        who()
    if "search" in command:
        search()
    if "play" in command:
        play()
    if "the date" in command:
        dates()
    if "the time" in command:
        times()
    if "new note" in command:
        note()
    if "calculator" in command:
        calculator()
    if "weather" in command:
        weather()
    
    if 'mail' in command:
        mail()
    
    if 'dictate' in command:
        dictate()
        

    if "settings" in command:
        settings()
        
    if 'virus' in command or "covid" in command or 'coronavirus' in command:
        covid_counter()
    
    if 'news' in command:
        news()

    if 'file' in command:
        file()
        
    if 'place' in command:
        place_search()
            
            
#main
def main():
        listen()
        interpret()
        if nothing_key in command:
            listen()
            interpret()

                

def activate():
    main()



class commpage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="1) How are you?: Asks Assistant how he is\n2) Who are you?: Asks Assistant what he is\n3) Search: Assistant will ask what to search for and open in browser\n4) Play: Assistant will ask you what to play and search Youtube\n5) Place: Assistant will ask where and direct you to Google Maps\n6) What is the date?: Assistant will tell you the date\n7) What is the time?: Assistant will tell you the time\n8) New note: Assistant will open a new note\n9) Open Calculator: Assistant will open calculator\n10) How is the Weather: Assistant will ask you what city and\n      tell you the weather\n11) Settings: Assistant will ask what settings to change\n      Three options: speed, volume, and sound of Assistant\n12) Check my mail: Assistant will open Gmail\n13) Dictate a note: Assistant will ask you a name for the document\n      and will allow you to narrate the document, then will open\n      the document for you to see\n13) How many coronavirus cases are there: Assistant will direct you\n      to a live COVID-19 tracker\n14) Open a file: Assistant will let you choose to open\n      Document, Downloads, or Desktop\n\n\n **NOTE: These are not set functions, they include a keyword,\n     that will activate it. The keyword, is the most significant word\n      e.g. cronoavirus tracker, keyword = coronovirus/covid", font=LARGE_FONT, justify=LEFT)
        label.pack(pady=0,padx=0)


        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage)).place(x=480, y=0)
        


class listofcomm(tk.Tk):
    


    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, commpage, ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="", font=LARGE_FONT)
        label.pack(pady=200,padx=200)

        button = tk.Button(self, text="Don't know what to say?",
                            command=lambda: controller.show_frame(commpage)).place(x=430, y=0)
        
        button2 = tk.Button(self, text="Activate Assistant", height = 3, width = 15, 
                            command=lambda:activate()).place(x=220, y=300)
                
        
        def showImg(self):
            load = Image.open(path + "\\AI.jpg")
            render = ImageTk.PhotoImage(load)

            # labels can be text or images
            img = Label(self, image=render)
            img.image = render
            img.place(x=170, y=50)
        showImg(self)
        
app = listofcomm()
app.title("Primo")
app.mainloop()
