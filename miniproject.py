import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random,array
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from requests_html import HTMLSession
from PyQt5.QtGui import * 
from PyQt5.QtWebEngineWidgets import * 
from PyQt5.QtPrintSupport import * 
import os 
import speech_recognition as sr
import sys
import math
from pytube import YouTube
from PyDictionary import PyDictionary
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image      
from googletrans import Translator,LANGUAGES  
from tkinter import messagebox
import pyttsx3
import wikipedia
import pytesseract
import cv2
import numpy as np



from PyQt5.QtWebEngineWidgets import *
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)
        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        home_btn.triggered.connect(self.navigate_home)

        navtb.addSeparator()

        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        
        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-stop.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        sps_btn=QAction("Voice",self)
        sps_btn.setStatusTip("SPEAK AND SEARCH")
        sps_btn.triggered.connect(self.filemenu)
        navtb.addAction(sps_btn)

        txt_btn=QAction("TXTDET",self)
        txt_btn.setStatusTip("TEXT DETECTION")
        txt_btn.triggered.connect(self.test)
        navtb.addAction(txt_btn)

        cal_btn=QAction("Calculator",self)
        cal_btn.setStatusTip("Calculator")
        cal_btn.triggered.connect(self.calculator)
        navtb.addAction(cal_btn)

        pwd_btn=QAction("PwdGen",self)
        pwd_btn.setStatusTip("Password Generator")
        pwd_btn.triggered.connect(self.pwordGenn)
        navtb.addAction(pwd_btn)

        trn_btn=QAction("Translate",self)
        trn_btn.setStatusTip("translate")
        trn_btn.triggered.connect(self.trn)
        navtb.addAction(trn_btn)
        
        file_menu = self.menuBar().addMenu("&File")
        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        help_menu = self.menuBar().addMenu("&Help")
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),
                                            "Homepage", self)
        navigate_home_action.setStatusTip("Go to Spinn Design Homepage")
        help_menu.addAction(navigate_home_action)
        navigate_home_action.triggered.connect(self.navigate_home)
        dictionary_action = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-bottom.png')),
                                            "Dictionary", self)
        dictionary_action.setStatusTip("PyDict")
        help_menu.addAction(dictionary_action)
        dictionary_action.triggered.connect(self.pydictionary)
        ytdownload_action = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-bottom.png')),
                                            "YT Download", self)
        ytdownload_action.setStatusTip("PyYTDownloads")
        help_menu.addAction(ytdownload_action)
        ytdownload_action.triggered.connect(self.ytdownloads)

        self.setWindowTitle("Py Browser")
        self.setWindowIcon(QIcon(os.path.join('icons', 'cil-screen-desktop.png')))

        self.setStyleSheet("""QWidget{
           background-color: rgb(48, 48, 48);
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            top: -0.5em;
            color: rgb(255, 255, 255);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(90, 90, 90);
            border: 2px solid rgb(90, 90, 90);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(255, 255, 255);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
        }

        QLineEdit {
            border: 2px solid rgb(0, 36, 36);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(0, 36, 36);
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
        self.show()

    def ytdownloads(self):
        root = Tk()
        root.geometry("400x350")
        root.title("Youtube video downloader application")
        def download():
            try:
                myVar.set("Downloading...")
                root.update()
                YouTube(link.get()).streams.first().download()
                link.set("Video downloaded successfully")
            except Exception as e:
                myVar.set("Mistake")
                root.update()
                link.set("Enter correct link")
        Label(root, text="Welcome to youtube\nDownloader Application", font="Consolas 15 bold").pack()
        myVar = StringVar()
        myVar.set("Enter the link below")
        Entry(root, textvariable=myVar, width=40).pack(pady=10)
        link = StringVar()
        Entry(root, textvariable=link, width=40).pack(pady=10)
        Button(root, text="Download video", command=download).pack()
        root.mainloop() 

    def pydictionary(self):
        dictionary = PyDictionary()
        root = Tk()
        def dict():
	        meaning.config(text=dictionary.meaning(word.get())['Noun'][0])
	        synonym.config(text=dictionary.synonym(word.get())[0])
	        antonym.config(text=dictionary.antonym(word.get())[-5])
        Label(root, text="Dictionary", font=("Helvetica 20 bold"), fg="Green").pack(pady=10)

        frame = Frame(root)
        Label(frame, text="Type Word", font=("Helvetica 15 bold")).pack(side=LEFT)
        word = Entry(frame, font=("Helvetica 15 bold"))
        word.pack()
        frame.pack(pady=10)

        frame1 = Frame(root)
        Label(frame1, text="Meaning:- ", font=("Helvetica 10 bold")).pack(side=LEFT)
        meaning = Label(frame1, text="", font=("Helvetica 10"))
        meaning.pack()
        frame1.pack(pady=10)

        frame2 = Frame(root)
        Label(frame2, text="Synonym:- ", font=("Helvetica 10 bold")).pack(side=LEFT)
        synonym = Label(frame2, text="", font=("Helvetica 10"))
        synonym.pack()
        frame2.pack(pady=10)

        frame3 = Frame(root)
        Label(frame3, text="Antonym:- ", font=("Helvetica 10 bold")).pack(side=LEFT)
        antonym = Label(frame3, text="", font=("Helvetica 10"))
        antonym.pack(side=LEFT)
        frame3.pack(pady=10)

        Button(root, text="Submit", font=("Helvetica 15 bold"), command=dict).pack()

        root.mainloop()

    def calculator(self):
        def iCalc(source, side):
            storeObj = Frame(source, borderwidth=4, bd=4, bg="powder blue")
            storeObj.pack(side=side, expand =YES, fill =BOTH)
            return storeObj
        def button(source, side, text, command=None):
            storeObj = Button(source, text=text, command=command)
            storeObj.pack(side=side, expand = YES, fill=BOTH)
            return storeObj 
        class app(Frame):
            def __init__(self):
                Frame.__init__(self)
                self.option_add('*Font', 'arial 20 bold')
                self.pack(expand = YES, fill =BOTH)
                self.master.title('Calculator')   
                display = StringVar()
                Entry(self, relief=RIDGE, textvariable=display,justify='right', bd=30, bg="powder blue").pack(side=TOP, expand=YES, fill=BOTH)    
                for clearButton in (["C"]):
                    erase = iCalc(self, TOP)
                    for ichar in clearButton:
                        button(erase, LEFT, ichar, lambda storeObj=display, q=ichar: storeObj.set(''))
                for numButton in ("789/", "456*", "123-", "0.+"):
                    FunctionNum = iCalc(self, TOP)
                    for iEquals in numButton:
                        button(FunctionNum, LEFT, iEquals, lambda storeObj=display, q=iEquals: storeObj .set(storeObj.get() + q))
                EqualButton = iCalc(self, TOP)
                for iEquals in "=":
                    if iEquals == '=':
                        btniEquals = button(EqualButton, LEFT, iEquals)
                        btniEquals.bind('<ButtonRelease-1>', lambda e,s=self,
                                storeObj=display: s.calc(storeObj), '+')
                    else:
                        btniEquals = button(EqualButton, LEFT, iEquals,lambda storeObj=display, s=' %s ' % iEquals: storeObj.set(storeObj.get() + s))
            def calc(self, display):
                try:
                    display.set(eval(display.get()))
                except:
                    display.set("ERROR")
        if __name__=='__main__':
            app().mainloop()

    def trn(self):
        root = Tk()
        root.geometry("720*920")

        root.resizable(0,0)
        root.config(bg = 'ghost white')
        root.title("TRANSLATOR")
        Label(root, text = "LANGUAGE TRANSLATOR", font = "arial 20 bold", bg='white smoke').pack()
        Label(root,text ="Enter Text", font = 'arial 13 bold', bg ='white smoke').place(x=200,y=60)
        Input_text = Text(root,font = 'arial 10', height = 11, wrap = WORD, padx=5, pady=5, width = 60)
        Input_text.place(x=30,y = 100)
        Label(root,text ="Output", font = 'arial 13 bold', bg ='white smoke').place(x=780,y=60)
        Output_text = Text(root,font = 'arial 10', height = 11, wrap = WORD, padx=5, pady= 5, width =60)
        Output_text.place(x = 600 , y = 100)
        language = list(LANGUAGES.values())
        src_lang = ttk.Combobox(root, values= language, width =22)
        src_lang.place(x=20,y=60)
        src_lang.set('choose input language')
        dest_lang = ttk.Combobox(root, values= language, width =22)
        dest_lang.place(x=890,y=60)
        dest_lang.set('choose output language')
        def Translate():
            translator = Translator()
            translated=translator.translate(text= Input_text.get(1.0, END) , src = src_lang.get(), dest = dest_lang.get())

            Output_text.delete(1.0, END)
            Output_text.insert(END, translated.text)

        trans_btn = Button(root, text = 'Translate',font = 'arial 12 bold',pady = 5,command = Translate , bg = 'royal blue1', activebackground = 'sky blue')
        trans_btn.place(x = 490, y= 180 )
        root.mainloop()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2: 
            return

        self.tabs.removeTab(i)
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        f=open("a.txt","a")
        f.write('q')
        f.close() 
        self.urlbar.setCursorPosition(0)


    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)


    def navigate_to_url(self):     
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        f=open("a.txt",'a')
        ab=repr(q)
        f.write(ab + "\n")
        f.close()    

        self.tabs.currentWidget().setUrl(q)
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))


    def pwordGenn(self,digit):
        root =tk.Tk()
        root.geometry("300x300")
        root.title(" PWordGen ")
        text = tk.Text(root)
        MAX_LEN = 12
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']
 
        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>','*', '(', ')', '<']
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)
        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
        for x in range(MAX_LEN - 4):
            temp_pass = temp_pass + random.choice(COMBINED_LIST)
            temp_pass_list = array.array('u', temp_pass)
            random.shuffle(temp_pass_list)
        password = ""
        for x in temp_pass_list:
            password = password + x
        print(password)
        text.insert(tk.INSERT, password)
        b2 = tk.Button(root, text = "Exit",command = root.destroy)
        text.pack()
        b2.pack()
        root.mainloop()
        
  
    def test(self):
        url = "http://192.168.0.103:8080/video"
        pytesseract.pytesseract.tesseract_cmd= r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        font_scale=1.5
        font=cv2.FONT_HERSHEY_PLAIN
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            cap=cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open video")
        cntr=0;
        while True:
            ret,frame=cap.read()
            cntr=cntr+1;
            if ((cntr%20)==0):
                imgH,imgW,_ = frame.shape 
                x1,y1,w1,h1=0,0,imgH,imgW
                imgchar= pytesseract.image_to_string(frame)
                imgboxes=pytesseract.image_to_boxes(frame)
                for boxes in imgboxes.splitlines():
                    boxes=boxes.split(' ')
                    x,y,w,h=int(boxes[1]),int(boxes[2]),int(boxes[3]),int(boxes[4])
                    cv2.rectangle(frame,(x,imgH-y),(w,imgH-h),(0,0,255),3)
                cv2.putText(frame,imgchar,(x1+int(w1/50),y1+int(h1/50)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.imshow('Text Detection',frame)
                if cv2.waitKey(2)&0xFF==ord('q'):
                    break
       
        cap.release()
        cv2.destroyAllWindows()   
        
    def filemenu(self):
        r=sr.Recognizer()
        engine = pyttsx3.init()
        r.energy_threshold=5000
        with sr.Microphone() as source:
            print("Speak!")
            audio=r.listen(source)
            try:
                text=r.recognize_google(audio)
                print("You said : {}".format(text))
                url='https://www.google.co.in/search?q='
                search_url=url+text
                f=open("a.txt","a")
                f.write('search_url')
                f.close()
                self.tabs.currentWidget().setUrl(QUrl(search_url))

                result=wikipedia.summary(text, sentences =2 )
                print(result)
                engine.say(result)
                engine.runAndWait()   
            except:
                print("Can't recognize")

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()