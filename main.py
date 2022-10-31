import tkinter as tk
from tkinter import filedialog

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Degree Audit Planner")
button = tk.Button(root, text='Open', command=UploadAction)
button.pack()

root.mainloop()