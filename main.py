from time import sleep
import threading
import tkinter as tk
from tkinter import ttk

import time
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer


ip = "0.0.0.0"
port = 5000


def cetak():
    print("Bisa...")


tp9 = 0.0
tp10 = 0.0
af7 = 0.0
af8 = 0.0
au = 0.0
# data = []
# dict = {}
koneksi="=="

def eeg_handler(address, *args):
    global koneksi
    for arg in args:
        if arg==1:
            koneksi="Connected"
        else:
            koneksi="Disconnected"

def get_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.map("/muse/elements/touching_forehead", eeg_handler)
    return dispatcher

def main():

    dispatcher = get_dispatcher()
    server = ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    t_end = time.time() + 5 
    while time.time() < t_end:
        server.handle_request()
    print("selesai")
    print(koneksi)    

def clickBtn(l):
    print("mulai")
    t=threading.Thread(target=main)
    t.start()
    t.join()
    l.config(text=koneksi)
    print("apa ??")
    
window=tk.Tk()
window.geometry("600x400")
window.resizable(False,False)
frame=ttk.Frame(window)
labelDevice=ttk.Label(frame,text="Device :")
labelDevice.grid(row=0,column=0, padx=10,pady=10)

labelStatus=ttk.Label(frame,text="")
labelStatus.grid(row=0,column=1, padx=10,pady=10)
tombol_sapa = ttk.Button(frame,text="start",command=lambda : clickBtn(labelStatus))
tombol_sapa.grid(row=1,column=0,padx=10, pady=10)

frame.pack()

window.mainloop()