import tkinter as tk
from tkinter import ttk
from processList import *

win = tk.Tk()
win.title("Python")
#win.resizable(False, False)
win.geometry("1300x710+100+100")

row_format ="{:<10}  {:>30} " # left or right align, with an arbitrary '8' column width 
module_format = "{:<10}  {:>60} {:>80} {:>100} {:>90}"
module_format2 = "{:<10}  {:>50} {:>70} {:>80} {:>50}"
table = []
headers = ["PID", "Process"]
moduleheaders = ["DLL", "Path", "Version", "Company Name", "WinTrust" ]
frmcur_text = tk.StringVar()

def insertitem():
	table = ProcessList()
	for items in table:
		listbox.insert(tk.END, row_format.format(*items, sp=" "*2))

def onSelect(event):
	w = event.widget
	index = int(w.curselection()[0])
	value = w.get(index).split()[0]
	listbox2.delete('0', 'end')
	modules = ModuleList(int(value))
	listbox2.insert(0, module_format.format(*moduleheaders, sp=" "*2))
	for items in modules:
		listbox2.insert(tk.END, module_format2.format(*items, sp=" "*2))
	

buttons_frame = ttk.Frame(win)
buttons_frame.grid(column=0, row=0, padx=8, pady=4, sticky=tk.W+tk.E) 

button = tk.Button(buttons_frame, text = "Load", command = insertitem)
button.grid(column = 0, row = 0,  sticky=tk.W+tk.E)

mighty = ttk.LabelFrame(win, text=' Processes ')
mighty.grid(column=0, row=1, padx=8, pady=4, sticky = tk.W+tk.E)

listbox = tk.Listbox(mighty, width = 210, height = 20)
listbox.grid(column = 0, row = 0)
listbox.bind('<<ListboxSelect>>', onSelect)

scrollbar = tk.Scrollbar(mighty,orient="vertical")
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)
listbox.insert(0, row_format.format(*headers, sp=" "*2))
scrollbar.grid(row=0, column=1, sticky='ns')

listbox2 = tk.Listbox(mighty, width = 210, height = 20)
listbox2.grid(column = 0, row = 1)

scrollbar2 = tk.Scrollbar(mighty, orient="vertical")
scrollbar2.config(command=listbox2.yview)
listbox2.config(yscrollcommand=scrollbar2.set)
scrollbar2.grid(row=1, column=1, sticky='ns')

listbox2.insert(0, module_format.format(*moduleheaders, sp=" "*2))

win.mainloop()