import tkinter as tk
from tkinter import StringVar, colorchooser, filedialog, ttk

import darkdetect
import matplotlib.font_manager
import sv_ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk

filename = "images/default_img.jpeg"
# Position
x = 50
y = 50
angle = 0.0
# Color
r = 255
g = 255
b = 255
hex_code = "#ff0000"
opacity = 255


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
    print(filename)
    if not filename:
        filename = "images/default_img.jpeg"
    image = Image.open(filename).convert("RGBA")
    # Fit it in a size
    image.thumbnail((720, 720))
    # Update the image to display again.
    image_pi = ImageTk.PhotoImage(image)
    image_on_display.config(image=image_pi)


def get_color():
    global r, g, b, hex_code

    color = colorchooser.askcolor(initialcolor="#ff0000")
    r = color[0][0]
    g = color[0][1]
    b = color[0][2]

    hex_code = color[1]

    text_color_display.config(background=hex_code)


def watermark_text(save_as=""):
    global image_pi, opacity, angle
    # Text
    text = text_entry.get() or "Watermark"

    # Text Font
    font = fonts_dict.get(text_font_combobox.get(), "/home/rafinlinux/.fonts/arial.ttf")

    # Text Font Size
    # print(size_spinbox_value.get())
    size = int(size_spinbox_value.get()) or 30

    # Text Font Color Opacity
    # print(opacity_spinbox_value.get())
    opacity = int(
        "255"
        if opacity_spinbox_value.get() == ""
        else opacity_spinbox_value.get().split(".")[0]
    )

    # Create Image drawer to draw
    image = Image.open(filename).convert("RGBA")
    image.thumbnail((720, 720))
    # print(image.size)

    # Create a larger canvas for both image and text
    canvas_size = (image.size[0] + 100, image.size[1] + 100)
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

    # Paste original image in center of canvas
    paste_x = 50  # half of the extra 100 pixels
    paste_y = 50
    canvas.paste(image, (paste_x, paste_y))

    # make a blank image for the text, initialized to transparent text color
    # txt = Image.new("RGBA", [image.size[0] + 100,image.size[1] + 100], (0, 0, 0, 0))
    txt = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

    # get a drawing context
    draw = ImageDraw.Draw(txt)

    # get a font
    font = ImageFont.truetype(font, size)
    draw.text((x, y), text, font=font, fill=(r, g, b, opacity))

    rotated_txt = txt.rotate(angle, expand=0)
    out = Image.alpha_composite(canvas, rotated_txt)
    # out.show()
    out = out.crop((50, 50, image.size[0] + 50, image.size[1] + 50)).resize(
        (image.size), resample=Image.Resampling.LANCZOS
    )
    # cropped_example.show()
    image_pi = ImageTk.PhotoImage(out)
    image_on_display.config(image=image_pi)

    if save_as:
        rgb_img = out.convert("RGB")
        rgb_img.save(save_as)


def save_image_as():
    save_filename = filedialog.asksaveasfilename()
    watermark_text(save_as=save_filename)


def go_up():
    global y
    y = y - 5
    watermark_text()


def go_down():
    global y
    y = y + 5
    watermark_text()


def go_left():
    global x
    x = x - 5
    watermark_text()


def go_right():
    global x
    x = x + 5
    watermark_text()


def clockwise():
    global angle
    angle = angle + 1.0
    watermark_text()


def anticlockwise():
    global angle
    angle = angle - 1.0
    watermark_text()


def update_scl_lbl(val):
    v = int(val.split(".")[0]) or 255
    opacity_scale_value_label["text"] = v


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
open_file.grid(column=0, row=8, sticky=(tk.W))

# Get default image
image = Image.open(filename).convert("RGBA")
# Fit it in a size
image.thumbnail((720, 720))
# make a blank image for the text, initialized to transparent text color
txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
image_pi = ImageTk.PhotoImage(image)
image_frame = ttk.Frame(mainframe, height=720, width=720, borderwidth=2, relief="solid")
image_frame.grid(column=0, row=0, rowspan=8)
image_on_display = ttk.Label(image_frame, image=image_pi)
image_on_display.grid(column=0, row=0)

# Use this text
text_label = ttk.Label(mainframe, text="Watermark Text")
text_label.grid(column=1, row=0, sticky=(tk.E))
text_entry = ttk.Entry(mainframe, width=23)
text_entry.grid(column=2, columnspan=4, row=0, sticky=(tk.W))

# Text Font
text_font_label = ttk.Label(mainframe, text="Text Font")
text_font_label.grid(column=1, row=1, sticky=(tk.E))
text_font_combobox = ttk.Combobox(
    mainframe, width=20, values=list(sorted_fonts_dict.keys())
)
text_font_combobox.grid(column=2, columnspan=4, row=1, sticky=(tk.W))

# Text Size
text_size_label = ttk.Label(mainframe, text="Font Size")
text_size_label.grid(column=1, row=2, sticky=(tk.E))
size_spinbox_value = StringVar()
text_size_spinbox = ttk.Spinbox(
    mainframe,
    # orient="horizontal",
    # length=200,
    from_=1,
    to=100,
    # variable=scale_value,
    textvariable=size_spinbox_value,
    # command=update_scl_lbl,
    width=3,
)
text_size_spinbox.grid(column=2, columnspan=4, row=2, sticky=(tk.W))
text_size_spinbox.set(30)
# scale_value_label = ttk.Label(mainframe, text="30")
# scale_value_label.grid(column=3, row=2)

# Text Color
text_color_label = ttk.Label(mainframe, text="Font Color")
text_color_label.grid(column=1, row=3, sticky=(tk.E))
text_color_display = ttk.Label(mainframe, width=2, background="#ff0000")
text_color_display.grid(column=2, columnspan=4, row=3, sticky=(tk.W))
text_color_btn = ttk.Button(mainframe, text="Choose", command=get_color)
text_color_btn.grid(column=3, row=3)


# Text Color Opacity
text_opacity_label = ttk.Label(mainframe, text="Color Opacity")
text_opacity_label.grid(column=1, row=4, sticky=(tk.E))
opacity_spinbox_value = StringVar()
text_opacity_scale = ttk.Scale(
    mainframe,
    orient="horizontal",
    length=230,
    from_=1,
    to=255,
    variable=opacity_spinbox_value,
    command=update_scl_lbl,
)
text_opacity_scale.grid(column=2, columnspan=4, row=4, sticky=(tk.W))
opacity_scale_value_label = ttk.Label(mainframe, text="255")
opacity_scale_value_label.grid(column=6, row=4, sticky=(tk.W))

# Change x and y to change Positions
# Go up
position_label = ttk.Label(mainframe, text="Position")
position_label.grid(column=1, row=6, sticky=(tk.E))

go_up_btn = ttk.Button(mainframe, text="▲", command=go_up)
go_up_btn.grid(column=3, row=5)

go_right_btn = ttk.Button(mainframe, text="►", command=go_right)
go_right_btn.grid(column=4, row=6)

go_down_btn = ttk.Button(mainframe, text="▼", command=go_down)
go_down_btn.grid(column=3, row=7)

go_left_btn = ttk.Button(mainframe, text="◄", command=go_left)
go_left_btn.grid(column=2, row=6)

rotate_clockwise = ttk.Button(mainframe, text="⟳", command=clockwise)
rotate_clockwise.grid(column=5, row=6)

rotate_anticlockwise = ttk.Button(mainframe, text="↺", command=anticlockwise)
rotate_anticlockwise.grid(column=6, row=6)


# Show Text
update_text_btn = ttk.Button(mainframe, text="Update Text", command=watermark_text)
update_text_btn.grid(column=3, row=8)

# Save Image
save_image_btn = ttk.Button(mainframe, text="Save Image", command=save_image_as)
save_image_btn.grid(column=0, row=8, sticky=(tk.E))

# Global Padding on all child widgets of mainframe
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
