import tkinter as tk
from tkinter import IntVar, StringVar, filedialog, ttk

import darkdetect
import matplotlib.font_manager
import sv_ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk

filename = "images/default_img.jpeg"
x = 50
y = 50


# Getting the fonts available on the system.
unformatted_fonts_path_list = matplotlib.font_manager.findSystemFonts(
    fontpaths=None, fontext="ttf"
)
formatted_fonts_path_list = [x.split("\\")[-1] for x in unformatted_fonts_path_list]
fonts_list = [x.split("/")[-1].split(".")[:-1][0] for x in formatted_fonts_path_list]
fonts_dict = {k: v for (k, v) in zip(fonts_list, formatted_fonts_path_list)}
keys = list(fonts_dict.keys())
keys.sort()
# Sorted Dictionary
sorted_fonts_dict = {i: fonts_dict[i] for i in keys}


def get_image():
    global image_pi
    global filename

    # Get image to draw on
    filename = filedialog.askopenfilename()
    image = Image.open(filename)
    # Fit it in a size
    image.thumbnail((720, 720))
    # Update the image to display again.
    image_pi = ImageTk.PhotoImage(image)
    image_on_display.config(image=image_pi)


def watermark_text():
    global image_pi
    # Text
    text = text_entry.get() or "Watermark"

    # Text Font
    font = fonts_dict.get(text_font_combobox.get(), "/home/rafinlinux/.fonts/arial.ttf")

    # Text Font Size
    size = int(scale_value.get().split(".")[0]) or 30

    # Create Image drawer to draw
    image = Image.open(filename)
    image.thumbnail((720, 720))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, size)
    draw.text((x, y), text, font=font)

    # Update the image to display again.
    image_pi = ImageTk.PhotoImage(image)
    image_on_display.config(image=image_pi)


def scale_moved():
    pass

def update_scl_lbl(val):
    v = int(val.split(".")[0]) or 30
    scale_value_label["text"] = v

# Root
root = tk.Tk()
sv_ttk.set_theme(darkdetect.theme())
root.title("Image Watermarking Program")

# Mainframe
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Style
s = ttk.Style()

# Open image file
open_file = ttk.Button(mainframe, text="Open Image", command=get_image)
open_file.grid(column=0, row=4)

# Get default image
image = Image.open(filename)
# Fit it in a size
image.thumbnail((720, 720))
image_pi = ImageTk.PhotoImage(image)
image_frame = ttk.Frame(mainframe, height=720, width=720, borderwidth=2, relief="solid")
image_frame.grid(column=0, row=0, rowspan=4)
image_on_display = ttk.Label(image_frame, image=image_pi)
image_on_display.grid(column=0, row=0)

# Use this text
text_label = ttk.Label(mainframe, text="Watermark Text")
text_label.grid(column=1, row=0)
text_entry = ttk.Entry(mainframe)
text_entry.grid(column=2, row=0)

# Text Font
text_font_label = ttk.Label(mainframe, text="Text Font")
text_font_label.grid(column=1, row=1)
text_font_combobox = ttk.Combobox(mainframe, values=list(sorted_fonts_dict.keys()))
text_font_combobox.grid(column=2, row=1)

# Text Size
text_size_label = ttk.Label(mainframe, text="Text Font Size")
text_size_label.grid(column=1, row=2)
scale_value = StringVar()
text_size_scale = ttk.Scale(
    mainframe,
    orient="horizontal",
    length=200,
    from_=1,
    to=100,
    variable=scale_value,
    command=update_scl_lbl
)
text_size_scale.grid(column=2, row=2)
text_size_scale.set(30)
scale_value_label = ttk.Label(mainframe, text="30")
scale_value_label.grid(column=3, row=2)


# Show Text
show_text_btn = ttk.Button(mainframe, text="Show Text", command=watermark_text)
show_text_btn.grid(column=1, row=9, columnspan=2)


# Global Padding on all child widgets of mainframe
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
