from tkinter import *
from tkinter import ttk

root=Tk()
root.grid_anchor("center")

style = ttk.Style()

style.theme_use("clam")
style.configure("Fancy.TButton", foreground="white", background="#ff0091")

btn1 = ttk.Button(root,style="Fancy.TButton")
btn1.grid(row=0, column=0, pady=5)

btn2 = ttk.Button(root, text='Button 2', padding=10, width=20)
btn2.grid(row=1, column=0, pady=5)

btn3 = ttk.Button(root, text='Button 3', padding=10, width=20, style="Fancy.TButton")
btn3.grid(row=2, column=0, pady=5)

root.mainloop()