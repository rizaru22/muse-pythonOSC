import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd

class Tabel(tk.Tk):
    #class Variable
    filepath = 'project/ujicoba/training.csv'

    def __init__(self):
        super().__init__()
        self.title("Aplikasi EEG -- DataFrame")
        self.geometry("600x400")
        frame=tk.Frame(self,width=200,height=50)
        frame.pack(fill=None,expand=False)
        df=pd.read_csv(Tabel.filepath)
        df['Label']=df['Label'].replace([0.0,1.0,2.0,3.0],['fear','sad','joy','anger'])
        self.table = Table(frame,dataframe=df, showtoolbar=True, showstatusbar=True)
        self.table.show()

df=Tabel()
df.mainloop()