import tkinter as tk
from tkinter import PhotoImage, colorchooser, filedialog, ttk

import darkdetect
import sv_ttk
from PIL import Image, ImageTk
from PIL.ImageFile import ImageFile


def get_image():
    global pi_img

    filename = filedialog.askopenfilename()
    img = Image.open(filename)
    pi_img = ImageTk.PhotoImage(img)
    opened_img.config(image=pi_img)


def get_set_color():
    global style
    get_color = colorchooser.askcolor(initialcolor="#ff0000")[1]
    print(get_color)
    style.map(
        "WT_COLOR.TButton",
        # foreground=[("!active", "black"), ("pressed", "red"), ("active", "white")],
        background=[
            ("!active", get_color),
            ("pressed", get_color),
            ("active", get_color),
        ],
    )
    text_entry.configure(foreground=get_color)
    color_btn.configure(style="WT_COLOR.TButton")


# Window setup
root = tk.Tk()
style = ttk.Style()
style.theme_use("clam")
root.title("Image Watermarking Program")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# sv_ttk.set_theme(darkdetect.theme())

# Widgets
## Title
logo_name = ttk.Label(mainframe, text="Make It Yours!", font="TkHeadingFont")
logo_name.grid(column=0, row=0, columnspan=3, sticky=tk.N)

## Image widgets
open_file = ttk.Button(mainframe, text="Open Image", command=get_image)
open_file.grid(column=0, row=3)

default_img = Image.open("Images/deafult_img.jpeg").resize(
    (1280, 720), Image.Resampling.LANCZOS
)
default_img_PI = ImageTk.PhotoImage(default_img)
opened_img = ttk.Label(mainframe, image=default_img_PI)
opened_img.grid(column=0, row=1, rowspan=2)

## Watermark widgets
text_label = ttk.Label(mainframe, text="Watermark Text")
text_label.grid(column=1, row=1)
text_entry = ttk.Entry(mainframe)
text_entry.grid(column=2, row=1)

### Watermark Text Color
color_label = ttk.Label(mainframe, text="Text Color")
color_label.grid(column=1, row=2)
color_btn = ttk.Button(mainframe, command=get_set_color, width=2)
color_btn.grid(column=2, row=2)

# Global Padding on all child widgets of mainframe
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
