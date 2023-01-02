import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading
import time

import csv
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer



class Setting(tk.Tk):
    #class Variable

    def __init__(self):
        super().__init__()
        self.emotion=StringVar()
        self.title("Aplikasi EEG -- Settings")
        self.geometry("400x400")
        #label
        self.labelName=ttk.Label(self,text="Name")
        self.labelName.grid(row=0,column=0,padx=10,pady=10)
        
        #input
        self.inputName=ttk.Entry(self)
        self.inputName.grid(row=0,column=1,padx=10,pady=10)
        
        #label
        self.labelEmotion=ttk.Label(self,text="Choose an emotion :")
        self.labelEmotion.grid(row=1,column=0, columnspan=2, padx=10,pady=10,sticky="NS")
        
        #radioButton
        
        self.rbFear=ttk.Radiobutton(self,text="Fear",variable=self.emotion,value="Fear")
        self.rbFear.grid(row=2,column=0,padx=10,pady=10,sticky="W")
        
        self.rbAnger=ttk.Radiobutton(self,text="Anger",variable=self.emotion,value="Anger")
        self.rbAnger.grid(row=2,column=1,padx=10,pady=10,sticky="W")
        
        self.rbJoy=ttk.Radiobutton(self,text="Joy",variable=self.emotion,value="Joy")
        self.rbJoy.grid(row=3,column=0,padx=10,pady=10,sticky="W")
        
        self.rbSad=ttk.Radiobutton(self,text="Sad",variable=self.emotion,value="Sad")
        self.rbSad.grid(row=3,column=1,padx=10,pady=10,sticky="W")
        
        
        #button
        self.buttonEnter=ttk.Button(self,text="Record",command=self.record)
        self.buttonEnter.grid(row=4,column=0,columnspan=2,padx=10,pady=10,sticky="NS")
        
    def record(self):
        name=self.inputName.get()
        emotion=self.emotion.get()
        print(name + " Has Emotion :" + str(emotion))
        self.destroy()
        self.record=eegRecord(name,emotion)
        self.record.mainloop()
        
        
        
        
        
class eegRecord(tk.Tk):
    #class Variable
    ip="0.0.0.0"
    port=5000
    tp9=0.0
    af7=0.0
    af8=0.0
    tp10=0.0
    au=0.0
    
    def __init__(self,name,emotion):
        super().__init__()
        
        self.title("Aplikasi EEG -- Check Connection")
        self.geometry("600x400")
        # self.resizable(False,False)
        self.name=name
        self.emotion=emotion
        #label
        self.labelName=ttk.Label(self,text=self.name)
        self.labelName.grid(row=0,column=0,padx=10,pady=10,sticky="W")
            
        
        self.labelEmotion=ttk.Label(self,text=":"+self.emotion)
        self.labelEmotion.grid(row=0,column=1,padx=10,pady=10,sticky="W")
        
        #label
        self.labelDevice=ttk.Label(self,text="Device ")
        self.labelDevice.grid(row=1,column=0,padx=10,pady=10,sticky="W")
            
        
        self.labelConnection=ttk.Label(self,text=":")
        self.labelConnection.grid(row=1,column=1,padx=10,pady=10,sticky="W")
        
        self.labelChannel=ttk.Label(self,text="Channel")
        self.labelChannel.grid(row=2,column=0,columnspan=2,padx=10,pady=10,sticky="NS")
        
        self.labelTP9=ttk.Label(self,text="TP9 ")
        self.labelTP9.grid(row=3,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueTP9=ttk.Label(self,text=":")
        self.labelValueTP9.grid(row=3,column=1,padx=10,pady=10,sticky="W")
        
        self.labelTP10=ttk.Label(self,text="TP10 ")
        self.labelTP10.grid(row=4,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueTP10=ttk.Label(self,text=":")
        self.labelValueTP10.grid(row=4,column=1,padx=10,pady=10,sticky="W")
        
        self.labelAF7=ttk.Label(self,text="AF7 ")
        self.labelAF7.grid(row=5,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueAF7=ttk.Label(self,text=":")
        self.labelValueAF7.grid(row=5,column=1,padx=10,pady=10,sticky="W")
        
        self.labelAF8=ttk.Label(self,text="AF8 ")
        self.labelAF8.grid(row=6,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueAF8=ttk.Label(self,text=":")
        self.labelValueAF8.grid(row=6,column=1,padx=10,pady=10,sticky="W")
        
        
        
        
        
        #button
        self.buttonStart=ttk.Button(self,text="Start",command=self.startAction)
        self.buttonStart.grid(row=6,column=0,columnspan=2,padx=10,pady=10,sticky="NS")
        
    def startAction(self):
        self.filePath=''
        
        if self.emotion=='Anger':
            self.filePath='project/anger/'
        elif self.emotion=='Fear':
            self.filePath='project/fear/'
        elif self.emotion=='Joy':
            self.filePath='project/joy/'
        elif self.emotion=='Sad':
            self.filePath='project/sad/'
        self.filePathName=self.filePath+self.name+'.csv'
        
        self.buttonStart.config(state=tk.DISABLED)
        thread=threading.Thread(target=self.init_main)
        thread.start()
        self.checkThread(thread)
        
    def checkThread(self,thread):
        if thread.is_alive():
            self.check=self.after(500,lambda:self.checkThread(thread))
        else:
            self.buttonStart.config(state=tk.NORMAL)
            
    
    def init_main(self):
        self.listJoin=[]
        self.dispatcher=Dispatcher()
        self.dispatcher.map("/muse/elements/touching_forehead", self.handler)
        self.dispatcher.map("/muse/eeg", self.eeg_handler)
        
        self.server=ThreadingOSCUDPServer((eegRecord.ip,eegRecord.port),self.dispatcher)
        print("Listening on UDP port "+str(eegRecord.port))
        t_end = time.time() + 10 
        while time.time() < t_end:
            self.server.handle_request()
        self.server.server_close()
        with open(self.filePathName,'w',newline='') as self.f:
            self.writer=csv.writer(self.f,lineterminator='\n')
            self.writer.writerows(self.listJoin)
        print("selesai")

    def handler(self,address,*args):
        for arg in args:
            # print (arg)
            if arg == 1:
                self.labelConnection.config(text=": Connected")
            else:
                self.labelConnection.config(text=": Disconnected")
            
    def eeg_handler(self, address, *args):
        eegRecord.tp9, eegRecord.af7, eegRecord.af8, eegRecord.tp10, eegRecord.au = args
        
        self.labelValueTP9.config(text=":"+str(eegRecord.tp9))
        self.labelValueTP10.config(text=":"+str(eegRecord.tp10))
        self.labelValueAF7.config(text=":"+str(eegRecord.af7))
        self.labelValueAF8.config(text=":"+str(eegRecord.af8))
        self.data=[eegRecord.tp9,eegRecord.af7,eegRecord.af8,eegRecord.tp10]
        self.listJoin.append(self.data)
        # print(type(self.list))
        # self.listData.append(self.data)
        
            # self.writer.writerow('\n')
        

# app=Intro()
# app.mainloop()

s=Setting()
s.mainloop()