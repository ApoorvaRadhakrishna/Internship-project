from chatterbot import ChatBot
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pyttsx3 as pt
import speech_recognition as s
import threading

# we are initiating engine to talk
talk = pt.init()
# audio contains list of voices
audio = talk.getProperty('voices')
print(audio)
# we here set voice
talk.setProperty('voice', audio[1].id)
dataset_dict = ''


def speak(statement):
    talk.say(statement)
    talk.runAndWait()


# define a name for the chat box
bot = ChatBot("My Bot")

# to create another window
main = tk.Tk()
# setting size for another window
main.geometry("1600x900")
# to set title of the window
main.title("My Chat bot")
# to set background color
main.config(bg="#913f92")
# to open the photo or image in another window
image = ImageTk.PhotoImage(Image.open("C:/Users/admin/Desktop/DLITHE_INTERNSHIP/datasets/chatbot1.png"))
photolabel = Label(main, image=image)
photolabel.pack(pady=5)


def traindata():
    # importing json library
    import json
    # reading json file
    dataset = open("data.json")
    print(dataset)
    # load json data from the file
    dataset_dict = json.load(dataset)
    print('******************************Dataset Training Start**********************************')
    print(dataset_dict)
    print('-------------------------')
    # reading intents
    for i in dataset_dict['intents']:
        print(i)
    print('-------------------------')
    try:

        for i in range(len(dataset_dict)):
            print(dataset_dict[0][0])
            print('-------------------------')
    except:
        print('')
    print('******************************Dataset Training End**********************************')


traindata()


# we define takequery function that takes voice as input and  voice is converted into string

def takequery():
    # reconizer recognise the audio from the user
    speechr = s.Recognizer()
    # seconds of non speaking is considered as complete we have set it to 1
    speechr.pause_threshold = 1
    print("speak! bot is listening")
    with s.Microphone() as micro:
        try:
            # it recognize the audio from microphone and stores in voice variable
            voice = speechr.listen(micro)
            # here audio get coverted into string using google
            string1 = speechr.recognize_google(voice, language='eng-in')
            # we print here to see whether voice getting recognised correctly or not
            print(string1)
            speak("You said " + string1)
            try:
                print('******************************Using Dataset**********************************')
                print(dataset_dict)
                print('-------------------------')
                # reading intents
                for i in dataset_dict['intents']:
                    print(i)
                print('-------------------------')

                for i in range(len(dataset_dict)):
                    print(dataset_dict[0][0])
                    print('-------------------------')
            except:
                print('')
            if string1 == "stop":
                speak("I am stopping the process")
                quit()
            # here the string is entering the text field
            textf.delete(0, END)
            textf.insert(0, string1)
            enter()
        except Exception as e:
            speak("not recognized plesase speak again")


# fuction enter created in button
def enter():
    query = textf.get()
    ans = bot.get_response(query)
    # end is used for new line
    msgs.insert(END, "you : " + query)
    # answer is of type statement hence we need to convert into string
    msgs.insert(END, "bot : " + str(ans))
    # calling function speak
    speak(ans)
    # to clear the text field
    textf.delete(0, END)
    # to scroll to the end to read messages
    msgs.yview(END)


# to create a message box
frame = Frame(main)

# to create scroll bar
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
# setting scroll bar to right
sc.pack(side=RIGHT, fill=Y)
# setting messages to left
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack(pady=5)

# creating text field
textf = Entry(main, font=("Calibri", 22))
textf.pack(padx=10, pady=10)

# create a button
btn = Button(main, text="enter", font=("Calibri", 22), command=enter)
btn.pack(pady=5)


# creating a enter function so that it can sens messages when enter is pressed in keyboard
def enter_function(event):
    btn.invoke()


# binding enter key with main window
main.bind('<Return>', enter_function)


# to run the function mutiple times we use
def repeatlistening():
    while True:
        takequery()


# here threading is uded because the function is called on main thread hence main window is not visible as it gets
# busy executing query
t = threading.Thread(target=repeatlistening)
t.start()
main.mainloop()
