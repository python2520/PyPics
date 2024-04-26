import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk

# UI
root = tk.Tk()
root.geometry("1000x600")
root.title("Photo Editor")
root.config(bg="white")

# Global variables
pen_color = "black"
pen_size = 5
file_path = ""
brightness_value = 1.0

# ALLOWS USERS TO EDIT AN IMAGE OF THEIR CHOICE
def add_image():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image")  # file directory for pics 
    if file_path:
        image = Image.open(file_path) # open image from file path
        # resize image
        width, height = int(image.width / 2), int(image.height / 2)
        image = image.resize((width, height), Image.BILINEAR) # <- BILINEAR is in pillow
        canvas.config(width=image.width, height=image.height)
        image = ImageTk.PhotoImage(image) # in pillow as well
        # set image to canvas
        canvas.image = image
        canvas.create_image(0, 0, image=image, anchor="nw")
        # enable filter combobox
        toggle_filter_combobox("normal")
        # enable save button
        save_button.config(state="normal")
        # enable brightness slider
        brightness_slider.config(state="normal")

# Change the brightness of the image
def change_brightness(value):
    global brightness_value
    brightness_value = float(value)
    apply_filter("Brightness")

def change_color():
    global pen_color
    # shows a color palette 
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_size(size):
    global pen_size
    pen_size = size

# ENABLES PEN DRAWING
def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='') # creates a bunch of ovals as line drawings

def clear_canvas():
    canvas.delete("all")
    # disable filter combobox initially 
    toggle_filter_combobox("disabled")
    # disable save button
    save_button.config(state="disabled")
    # disable brightness slider
    brightness_slider.config(state="disabled")

# FILTER PRESETS
def apply_filter(filter):
    if not file_path:
        return
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.BILINEAR) # <- In pillow imports
    if filter == "Black and White":
        image = ImageOps.grayscale(image)
    elif filter == "Blur":
        image = image.filter(ImageFilter.BLUR)
    elif filter == "Sharpen":
        image = image.filter(ImageFilter.SHARPEN)
    elif filter == "Smooth":
        image = image.filter(ImageFilter.SMOOTH)
    elif filter == "Emboss":
        image = image.filter(ImageFilter.EMBOSS)
    elif filter == "Brightness":
        image = ImageEnhance.Brightness(image).enhance(brightness_value)

    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# allow the filter combobox to appear ONLY when an image is selected
def toggle_filter_combobox(state):
    filter_combobox.config(state=state)

# ability to save edited image
def save_image():
    if not file_path:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        canvas.postscript(file=save_path + '.eps') 
        img = Image.open(save_path + '.eps') 
        img.save(save_path) # save as desired format (e.g., .png)

# creates left frame
left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

# canvas size
canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

# Image Button
image_button = tk.Button(left_frame, text="Upload Image", command=add_image, bg="white")
image_button.pack(pady=15)

# Color Button
color_button = tk.Button(
    left_frame, text="Change Pen Color", command=change_color, bg="white")
color_button.pack(pady=5)

# Pen Size 
pen_size_frame = tk.Frame(left_frame, bg="white")
pen_size_frame.pack(pady=5)

# PEN SIZE RADIO BUTTONS:
# small pen
pen_small = tk.Radiobutton(
    pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="white") 
pen_small.pack(side="left")

# medium pen
pen_medium = tk.Radiobutton(
    pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="white")
pen_medium.pack(side="left")
pen_medium.select()

# large pen
pen_large = tk.Radiobutton(
    pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="white")
pen_large.pack(side="left")

# Clear Button
clear_button = tk.Button(left_frame, text="Clear All",
                         command=clear_canvas, bg="#FF9797")
clear_button.pack(pady=10)

# Filter Combobox
filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur", "Emboss", "Sharpen", "Smooth"], state="disabled")
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>",
                     lambda event: apply_filter(filter_combobox.get()))

# Brightness Slider
brightness_label = tk.Label(left_frame, text="Brightness", bg="white")
brightness_label.pack()
brightness_slider = tk.Scale(left_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=change_brightness, state="disabled")
brightness_slider.pack()

# Save Button
save_button = tk.Button(left_frame, text="Save As", command=save_image, bg="white", state="disabled")
save_button.pack(pady=10)

# Draw motion
canvas.bind("<B1-Motion>", draw)

root.mainloop()
