# All the required libraries
from tkinter import *
from tkinter import colorchooser
from PIL import ImageTk, Image
from tkinter import messagebox
from difflib import get_close_matches
from tkinter.ttk import Combobox
from textblob import TextBlob
import pyttsx3
import speech_recognition as sr
import json


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate',150)


# Function for search button
def search():
    data = json.load(open('data.json'))
    wordEntered = enterWordEntry.get()

    wordEntered = wordEntered.lower()
    textarea.config(state=NORMAL)
    textarea.delete(1.0,END)

    if wordEntered in data:
        meaning = data[wordEntered]
        for item in meaning:
            textarea.insert(END,u'\u2192 '+item+'\n\n')
        textarea.config(state=DISABLED)

    elif len(get_close_matches(wordEntered,data.keys()))>0:
        close_match = get_close_matches(wordEntered,data.keys())[0]
        result = messagebox.askyesno('Confirm','Did you mean '+close_match+' ?')
        if result == True:
            meaning = data[close_match]
            for item in meaning:
                textarea.insert(END,u'\u2192 '+item+'\n\n')
            textarea.config(state=DISABLED)

        else:
            messagebox.showinfo('Information','Entered word does not exist.')
            enterWordEntry.delete(0, END)

    else:
        messagebox.showerror('Error','Entered word does not exist. Please double check it.')
        enterWordEntry.delete(0,END)


# Function for Microphone button of enter word
def wordAudio():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(enterWordEntry.get())
    engine.runAndWait()


# Function for Microphone button of meaning
def meaningAudio():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(textarea.get(1.0,END))
    engine.runAndWait()
    textarea.config(state=NORMAL)


# Function for Speaker button
def speaker():
    enterWordEntry.delete(0, END)
    textarea.config(state=NORMAL)
    textarea.delete(1.0, END)
    textarea.config(state=DISABLED)
    r = sr.Recognizer()
    print("Please Talk")
    with sr.Microphone() as source:
        audio = r.record(source, duration=3)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio)
            wordEntered = text.lower()
            enterWordEntry.insert(END,wordEntered+'\n\n')

        except:
            messagebox.showerror('Error', 'Sorry, Could not recognise. Please Try Again')


# Function for translate button
def translate():
    try:
        textarea.config(state=NORMAL)
        textarea.delete(1.0, END)
        word = TextBlob(variable1.get())
        lan = word.detect_language()
        lan_todict = language.get()
        lan_to = lang_dict[lan_todict]
        word = word.translate(from_lang=lan, to=lan_to)
        textarea.insert(END, word)
    except:
        messagebox.showerror("Error","Sorry, It's translation doesn't exist")


# Function for clear button
def clear():
    enterWordEntry.delete(0,END)
    textarea.config(state=NORMAL)
    textarea.delete(1.0,END)
    textarea.config(state=DISABLED)


# Function for exit button
def exit():
    res = messagebox.askyesno('Confirm','Do you want to exit?')
    if res == True:
        root.destroy()
    else:
        pass


# Code for tkinter for setting geometry and title
root = Tk()
root.geometry('1270x750+0+0')
root.title("Talking Dictionary")
root.resizable(0,0)


# Code for background image
image = Image.open("background (1).png")
resized = image.resize((1270,700),Image.ANTIALIAS)
bgImage = ImageTk.PhotoImage(resized)
bgLabel = Label(root,image=bgImage)
bgLabel.place(x=0,y=0)


# Code for Enter Word label
enterWordLabel = Label(root,text="Enter Word",font=('Copperplate Gothic Light',22,'bold'),fg="#c9363b",bg="#ebcead",borderwidth=5,relief="raised")
enterWordLabel.place(x=280,y=50)


# Code for Enter word Entry
variable1 = StringVar()
enterWordEntry = Entry(root,textvariable=variable1,font=('Helvetica',22,'bold'),fg="#cc9d68",borderwidth=8,relief=GROOVE,justify=CENTER)
enterWordEntry.place(x=205,y=130)
enterWordEntry.focus_set()


# Code for search button
searchImage = PhotoImage(file="search.png")
searchButton = Button(root,image=searchImage,borderwidth=0,cursor="hand2",command=search,width=50,height=50)
searchButton.place(x=190,y=206)


# Code for speaker button of enter word
speakerImage = PhotoImage(file="loud-speaker.png")
speakerButton = Button(root,image=speakerImage,borderwidth=0,cursor="hand2",command=wordAudio,width=50,height=50)
speakerButton.place(x=330,y=206)


# Code for microphone button
microphoneImage = PhotoImage(file="microphone.png")
microphoneButton = Button(root,image=microphoneImage,borderwidth=0,cursor="hand2",command = speaker,width=50,height=50)
microphoneButton.place(x=470,y=206)


# Code for translate word label
translateWordLabel = Label(root,text="Translate",font=('Copperplate Gothic Light',22,'bold'),fg="#c9363b",bg="#ebcead",borderwidth=5,relief="raised")
translateWordLabel.place(x=950,y=50)


# Code for translate button
translateImage = PhotoImage(file="translate.png")
translateButton = Button(root,image=translateImage,borderwidth=0,cursor="hand2",command = translate,width=50,height=50)
translateButton.place(x=1020,y=206)


# Code for Combo Box of languages
lang_dict = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
language = StringVar()
font_box = Combobox(root,textvariable=language,state='readonly',width=15,font=('Helvetica',22,'bold'))
font_box['values'] = [e for e in lang_dict.keys()]
font_box.current(37)
font_box.place(x=900,y=130)


# Code for meaning label
meaningLabel = Label(root,text="Meaning",font=('Copperplate Gothic Light',22,'bold'),fg="#c9363b",bg="#ebcead",borderwidth=5,relief="raised")
meaningLabel.place(x=315,y=280)


# Code for text area where meaning will be displayed
textarea = Text(root,font=('Helvetica',22,'bold'),fg="#cc9d68",borderwidth=8,relief=GROOVE,height=7,width=40,wrap="word")
textarea.place(x=90,y=340)


# Code for speaker button of Meaning
loud_speakerImage = PhotoImage(file="loud-speaker.png")
loud_speakerButton = Button(root,image=loud_speakerImage,borderwidth=0,cursor="hand2",command=meaningAudio,width=50,height=50)
loud_speakerButton.place(x=140,y=610)


# Code for clear button
clearImage = PhotoImage(file="clear.png")
clearButton = Button(root,image=clearImage,borderwidth=0,cursor="hand2",command=clear,width=50,height=50)
clearButton.place(x=380,y=610)


# Code for exit button
exitImage = PhotoImage(file="exit.png")
exitButton = Button(root,image=exitImage,borderwidth=0,cursor="hand2",command=exit,width=50,height=50)
exitButton.place(x=620,y=610)


root.mainloop()