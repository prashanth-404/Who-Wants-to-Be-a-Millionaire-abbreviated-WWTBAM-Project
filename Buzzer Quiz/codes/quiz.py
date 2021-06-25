
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import time
import gspread
import keyboard,mouse
import subprocess
import time
import speech_recognition as sr                         # Note that while running this script, the arduino serial monitor tab should be closed!
import serial
from gtts import gTTS
import os
from playsound import playsound

i = 0
                                      			        # pointer to answers list
option_A = 0
option_B = 0
option_C = 0
option_D = 0

ans = ["A","B","B","B","D","B"]            			        # list containing answers

serialcomm = serial.Serial('COM3',9600,timeout = 1)   		# depends on which port you plugged your arduino, 9600 is the baud rate

list = [["Grand Central Terminal, Park Avenue, New York is the world's?","A) Largest Railway station","B) Highest railway station","C) Longest Railway Station","D) None of the above"],
        ["Entomology is the science that studies?","A) Behaviour of human beings","B) Insects","C) The origin and history of technical and scientific terms","D) The formation of rocks"],
        ["Eritrea, which became the 182nd member of the UN in 1993, is in the continent of?","A) Asia","B) Africa","C) Europe","D) Australia"],
        ["Garampani sanctuary is located at?","A) Junagarh, Gujarat","B) Diphu, Assam","C) Kohima, Nagaland","D) Gangtok, Sikkim"],
        ["For which of the following disciplines is Nobel Prize awarded?","A) Physics and Chemistry","B) Physiology or Medicine","C) Literatue, Peace and Economics","D) All of the above"],
        ["Hitler party which came into power in 1933 is known as?","A) Labour Party","B) Nazi Party","C) Ku-Klux-Klan","D) Democratic Party"]]

i = 0


def first_question():      #Function to narrate the first question
    language = 'en'
    for x in range(5):
        myobj = gTTS(text=list[0][x], lang=language, slow=False)        
        myobj.save("welcome.mp3") 
        playsound('welcome.mp3')
        os.remove("welcome.mp3")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):    #This function creates the UI window using pyqt5 i.e all the qtlabels,titles, the image is set
        global i                      
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1900, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(10, -100, 1900, 1051))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("picture.jpeg"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.question = QtWidgets.QLabel(self.centralwidget)
        self.question.setGeometry(QtCore.QRect(200, 600, 1521, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.question.setFont(font)
        self.question.setScaledContents(True)
        self.question.setObjectName("question")
        self.option_a = QtWidgets.QLabel(self.centralwidget)
        self.option_a.setGeometry(QtCore.QRect(190, 740, 711, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.option_a.setFont(font)
        self.option_a.setScaledContents(True)
        self.option_a.setObjectName("option_a")
        self.option_c = QtWidgets.QLabel(self.centralwidget)
        self.option_c.setGeometry(QtCore.QRect(190, 850, 711, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.option_c.setFont(font)
        self.option_c.setScaledContents(True)
        self.option_c.setObjectName("option_c")
        self.option_b = QtWidgets.QLabel(self.centralwidget)
        self.option_b.setGeometry(QtCore.QRect(1040, 740, 701, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.option_b.setFont(font)
        self.option_b.setScaledContents(True)
        self.option_b.setObjectName("option_b")
        self.option_d = QtWidgets.QLabel(self.centralwidget)
        self.option_d.setGeometry(QtCore.QRect(1040, 850, 711, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.option_d.setFont(font)
        self.option_d.setScaledContents(True)
        self.option_d.setObjectName("option_d")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1900, 26))
        self.menubar.setObjectName("menubar")
        self.menuOperator = QtWidgets.QMenu(self.menubar)
        self.menuOperator.setObjectName("menuOperator")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)    
        self.actionNext_Question = QtWidgets.QAction(MainWindow)
        self.actionNext_Question.setObjectName("actionNext_Question")
        self.menuOperator.addAction(self.actionNext_Question)
        self.menubar.addAction(self.menuOperator.menuAction())

        self.retranslateUi(MainWindow)                      #Please note that all the code related to gui above is automatically generated by PyQt5
        QtCore.QMetaObject.connectSlotsByName(MainWindow)  
        
        self.actionNext_Question.triggered.connect(lambda: self.thread_start(MainWindow))

    def retranslateUi(self, MainWindow):                    #This function puts text on the pyqt5 window and displays the first question
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.question.setText(_translate("MainWindow", list[0][0]))
        self.option_a.setText(_translate("MainWindow", list[0][1]))
        self.option_c.setText(_translate("MainWindow", list[0][2]))
        self.option_b.setText(_translate("MainWindow", list[0][3]))
        self.option_d.setText(_translate("MainWindow", list[0][4]))
        self.menuOperator.setTitle(_translate("MainWindow", "Operator"))
        self.actionNext_Question.setText(_translate("MainWindow", "Next Question"))
        self.actionNext_Question.setStatusTip(_translate("MainWindow", "Go to next question"))
        self.actionNext_Question.setShortcut(_translate("MainWindow", "Ctrl+N"))
    
    def next_clicked(self,MainWindow):                       #This function is called to display the next question
        global i
        if(i < len(list)):
            _translate = QtCore.QCoreApplication.translate
            self.question.setText(_translate("MainWindow", list[i][0]))
            self.option_a.setText(_translate("MainWindow", list[i][1]))
            self.option_c.setText(_translate("MainWindow", list[i][2]))
            self.option_b.setText(_translate("MainWindow", list[i][3]))
            self.option_d.setText(_translate("MainWindow", list[i][4]))
            
    def display_poll(self,MainWindow):                       #This function is used for displaying the poll answers.
        global option_A
        global option_B
        global option_C
        global option_D
        _translate = QtCore.QCoreApplication.translate
        self.question.setText(_translate("MainWindow", "Here are the poll results: "))
        self.option_a.setText(_translate("MainWindow", "A) " + str(option_A) + " votes"))
        self.option_c.setText(_translate("MainWindow", "B) " + str(option_B) + " votes"))
        self.option_b.setText(_translate("MainWindow", "C) " + str(option_C) + " votes"))
        self.option_d.setText(_translate("MainWindow", "D) " + str(option_D) + " votes"))
        option_A = 0
        option_B = 0
        option_C = 0
        option_D = 0
            
    def thread_start(self,MainWindow):    #This function is used to start the thread for which begins the process of narration etc.
        first_question()
        self.worker = Worker_Thread()
        self.worker.start()               #The worker thread is started
        self.worker.update.connect(lambda: self.next_clicked(MainWindow))   #A signal is emitted from the thread to tell pyqt5 that the next question is to be displayed
        self.worker.poll.connect(lambda: self.display_poll(MainWindow))     #A signal is emitted from the thread to tell pyqt5 that the poll answers are to be displayed
            
class Worker_Thread(QThread):           #This is the thread class

    def Speakup(self):                  #This function is used to speak out the question and options located at index i in list initialized at the top
        global i
        language = 'en'                 #language is set to english
        for x in range(5):
            myobj = gTTS(text=list[i][x], lang=language, slow=False)        
            myobj.save("welcome.mp3")                                        #the audio is produced and saved as welcome.mp3
            playsound('welcome.mp3')                                         #the audio is then played from the mp3 file produced
            os.remove("welcome.mp3")                                         #the file is now deleted as it is not required anymore
			
    def Audience_poll(self):                                                 # This function is used to collect data from audience responses present in a google spreadsheet linked to google form
        global i
        gc = gspread.service_account(filename = 'poll_result.json')          # this line searches through the spreadsheet and collects data
        sh = gc.open_by_key('136W2FyCZ2PNRzPVMsQmZQiNGV7-Xk_KFgOajtm7OKyQ')  #the json file is accessed by this key
        worksheet = sh.sheet1 
        global option_A
        global option_B        
        global option_C
        global option_D
        res = worksheet.col_values(2)   
        #https://docs.google.com/forms/d/e/1FAIpQLSfd3_oWsVbZyPFmJ9jk1DD7wrb3oL2_1j2ctHPP0wvVt-hhKQ/viewform?usp=sf_link # this is the google form handed out to audience
        for j in res:
            if(j == 'A'):
                option_A+=1                  # we parse through all the responses and increase the respective option count
            elif(j == 'B'):
                option_B+=1
            elif(j == 'C'):
                option_C+=1
            elif(j == 'D'):
                option_D+=1
        print("option A :" + str(option_A))  # finally all the options are printed out
        print("option B :" + str(option_B))
        print("option C :" + str(option_C))
        print("option D :" + str(option_D))
        self.poll.emit(-1)
        time.sleep(10)
        self.update.emit(i)
        
    def Expert_option(self):                 # This function opens the installed zoom app and connects it to the professor

        subprocess.call("C:\\Users\\chaitanya\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")   # this line opens the Zom app

        time.sleep(3)

        coordinates = [[737,447],[950,497],[1164,813],[950,550],[1164,813]]              # these are the (x,y) coordinates of the mouse 

        for i in range(5):                                                               # Now, it parses through the list of coordinates 
        
            time.sleep(4)
            mouse.move(coordinates[i][0]-190,coordinates[i][1]-115)
            mouse.click()
            
            if i == 1:
                time.sleep(1)
                keyboard.write("967 6705 7115")                                          # this is the meeting ID
            
            elif i == 3:
                time.sleep(2)
                keyboard.write("718772")                                                 # this is the password to the zoom meeting
                
            elif i == 4:
                time.sleep(10)
        
        time.sleep(10)
        
    def recognize_it(self,x):                       			# this function when called takes in voice input for 6 seconds, checks if the option spoken out is correct or not,
                                           			            # and then writes data to the serial port bus accordingly
        r = sr.Recognizer()                                     # creates an object of recognizer type
        mic = sr.Microphone()                                   # creates an object of microphone type which has access to the microphone of pc/laptop
        
        global i
    
        with mic as source:

            print("Speak out the option")
            audio = r.record(source = mic,duration = 6)  		# takes input for 6 seconds and records it

            try:
                text = r.recognize_google(audio)     		    # google's nlp package is used to recognize the audio 
                print("You said :"+ str(text))

                if(text[0:6].lower() == "option" and text[9:14].lower() == "final"):  # takes into account only if the format is followed
            
                    i+=1
                
                    if(x.lower() == text[7].lower()):           # checks for option 

                        print("Correct Answer, well done")
                        serialcomm.write('1'.encode())          # writes 1 to arduino serial port bus when the option is correct
                        self.update.emit(i)
                        self.Speakup()

                    else:

                        print("Wrong answer")
                        serialcomm.write('0'.encode())          # writes 0 to arduino serial port bus when the option is wrong
                        self.update.emit(i)
                        self.Speakup()

                elif(text.lower() == "expert option"):          # calls the expert option function whenever interpreted
            
                    self.Expert_option()
                    self.recognize_it(x)
                
                elif(text.lower() == "audience poll"):          # calls the audience poll function whenever interpreted
                    self.Audience_poll()
                    self.recognize_it(x)
                
                elif(text[0:13].lower() == "double option"):    # takes in two options, and checks if any of them are correct
                
                    i+=1
                
                    if(text[14].lower() == x.lower() or text[20].lower() == x.lower()):
                
                        print("correct answer")
                        serialcomm.write('1'.encode())          # If correct, sends 1 to the arduino
                    
                    else:
                
                        print("Wrong answer")
                        serialcomm.write('0'.encode())          # If wrong, sends 0 to arduino
                    
                else:
            
                    print("Could'nt recognize...Come again")    # 
                    self.recognize_it(x)
                    
            except:
                print("Again dude, say it again")               # if voice is not recognizable it goes into a recursive phase(so that the program doesn't crash)
                self.recognize_it(x)
                
            
            
    update = pyqtSignal(int)
    poll = pyqtSignal(int)
    def run(self):
        global i
        while(1):
            y = serialcomm.readline().decode('utf-8')           # reads the data coming from arduino serial bus and stores it in y variable
            if y == str(1):
                self.update.emit(i)                             # If it detects 1,(which means that someone has pressed the buzzer) it calls the recognize it function
                self.recognize_it(ans[i])                       # increases the list pointer by 1, ie, moves to the next question
            if(i == len(ans)):                        		    # if i reaches end of list, then the loop breaks and the connection is closed...
                break
                


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv) #pyqt5 app is created
    MainWindow = QtWidgets.QMainWindow() #Mainwindow is created
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()     #MainWindow is shown
    sys.exit(app.exec_())   #The program exits as soon as all the windows are closed.
