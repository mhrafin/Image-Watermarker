import tkinter as tk
from tkinter import PhotoImage, filedialog, ttk

import sv_ttk
from PIL import Image, ImageTk
from PIL.ImageFile import ImageFile


def get_image():
    filename = filedialog.askopenfilename()
    type(filename)
    img = Image.open(filename)
    global pi_img
    pi_img = ImageTk.PhotoImage(img)

    global opened_img
    opened_img.config(image=pi_img)


# Window setup
root = tk.Tk()
root.title("Image Watermarking Program")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sv_ttk.set_theme("dark")

# Widgets
## Title
logo_name = ttk.Label(mainframe, text="Make It Yours!", font="TkHeadingFont")
logo_name.grid(sticky=tk.N)

## Image widgets
open_file = ttk.Button(mainframe, text="Open Image", command=get_image)
open_file.grid(column=0, row=2)

default_img = Image.open("Images/deafult_img.jpeg")
default_img = default_img.resize((1280, 720), Image.Resampling.LANCZOS)
default_img_PI = ImageTk.PhotoImage(default_img)
opened_img = ttk.Label(mainframe, image=default_img_PI)
opened_img.grid(column=0, row=1)


# Global Padding on all child widgets of mainframe
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
