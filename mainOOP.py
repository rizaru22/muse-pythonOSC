import tkinter as tk
from tkinter import ttk
import threading
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

ip="0.0.0.0"
port=5000
tp9=0.0
af7=0.0
af8=0.0
tp10=0.0
au=0.0

class Intro(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Aplikasi EEG -- Check Connection")
        self.geometry("600x400")
        # self.resizable(False,False)
        
        #label
        self.labelDevice=ttk.Label(self,text="Device ")
        self.labelDevice.grid(row=0,column=0,padx=10,pady=10,sticky="W")
            
        
        self.labelConnection=ttk.Label(self,text=":")
        self.labelConnection.grid(row=0,column=1,padx=10,pady=10,sticky="W")
        
        self.labelChannel=ttk.Label(self,text="Channel")
        self.labelChannel.grid(row=1,column=0,columnspan=2,padx=10,pady=10,sticky="NS")
        
        self.labelTP9=ttk.Label(self,text="TP9 ")
        self.labelTP9.grid(row=2,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueTP9=ttk.Label(self,text=":")
        self.labelValueTP9.grid(row=2,column=1,padx=10,pady=10,sticky="W")
        
        self.labelTP10=ttk.Label(self,text="TP10 ")
        self.labelTP10.grid(row=3,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueTP10=ttk.Label(self,text=":")
        self.labelValueTP10.grid(row=3,column=1,padx=10,pady=10,sticky="W")
        
        self.labelAF7=ttk.Label(self,text="AF7 ")
        self.labelAF7.grid(row=4,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueAF7=ttk.Label(self,text=":")
        self.labelValueAF7.grid(row=4,column=1,padx=10,pady=10,sticky="W")
        
        self.labelAF8=ttk.Label(self,text="AF8 ")
        self.labelAF8.grid(row=5,column=0,padx=10,pady=10,sticky="W")
        
        self.labelValueAF8=ttk.Label(self,text=":")
        self.labelValueAF8.grid(row=5,column=1,padx=10,pady=10,sticky="W")
        
        
        
        
        #button
        self.buttonStart=ttk.Button(self,text="Start",command=self.startAction)
        self.buttonStart.grid(row=6,column=0,columnspan=2,padx=10,pady=10,sticky="NS")
        
    def startAction(self):
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
        self.dispatcher=Dispatcher()
        self.dispatcher.map("/muse/elements/touching_forehead", self.handler)
        self.dispatcher.map("/muse/eeg", self.eeg_handler)
        
        self.server=ThreadingOSCUDPServer((ip,port),self.dispatcher)
        print("Listening on UDP port "+str(port))
        t_end = time.time() + 10 
        while time.time() < t_end:
            self.server.handle_request()
        self.server.server_close()   
        print("selesai")

    def handler(self,address,*args):
        for arg in args:
            # print (arg)
            if arg == 1:
                self.labelConnection.config(text=": Connected")
            else:
                self.labelConnection.config(text=": Disconnected")
            
    def eeg_handler(self, address, *args):
        tp9, af7, af8, tp10, au = args
        self.labelValueTP9.config(text=":"+str(tp9))
        self.labelValueTP10.config(text=":"+str(tp10))
        self.labelValueAF7.config(text=":"+str(af7))
        self.labelValueAF8.config(text=":"+str(af8))
        
        # print("tp9:"+str(tp9) + " "+"tp10:" + str(tp10) + " "+"af7:"+str(af7) + " "+"af8:"+str(af8))
            



app=Intro()
app.mainloop()