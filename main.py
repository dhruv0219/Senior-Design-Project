import tkinter as tk
from tkinter import filedialog
from tkinter import *
import audit_functions

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)

    audit_functions.audit_transcript(filename, "ds")
    


root = tk.Tk()
root.configure(bg='black')
root.geometry("400x400")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Degree Audit Planner")
button = tk.Button(root, text='Open', command=UploadAction)
button.pack()

options = ["Traditional", "Networks and Telecomunications", "Data Science", "Cybersecurity", "Intelligent Systems", "Interactive Computing", "Systems"]
clicked = StringVar()
clicked.set("Traditional")

drop = OptionMenu( root , clicked , *options )
drop.pack()

root.mainloop()