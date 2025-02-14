import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button, Frame, Scale, Label
import serial
import time
import platform
import json
import os 

MS_TO_NS = 1e6

start = time.time_ns()
plat = platform.system()

if plat == "Windows":
    PORT = "COM4"
elif plat == "macOS":
    # port = "/dev/tty.usbmodem6D8118A649481"
    PORT = "/dev/tty.usbmodem144101"
elif plat == "Linux":
    PORT = "/dev/ttyUSB0"

out = serial.Serial(PORT, baudrate=9600, timeout=1)

CFG_FILE_NAME = 'calibration.config'

# Function to update the webcam feed in the Tkinter window
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_frame)

def send_data(x, y):
        # start = time.time_ns()
        global start
        if (time.time_ns() - start) > (15 * MS_TO_NS):
            out.write(b'X%dY%d\n' %(x,y))   
            start = time.time_ns()

## TODO: do 

if os.path.exists(CFG_FILE_NAME):
    with open(CFG_FILE_NAME, 'r') as openfile:
        config_obj = json.load(openfile)
else:
    
    config_obj = {'bottom_left': [0, 180], 'bottom_right': [180, 180], 
                  'top left': [0, 0], 'top right': [180, 0]}

x = 90
y = 90

# def on_slider_change_horiz(xs):
#     x = int(xs)
#     send_data(x,y)

# def on_slider_change_vert(ys):
#     global y
#     y = int(ys)
#     send_data(x,y)

def on_slider_change(value):
    global x, y
    x = int(horizontal_slider.get())
    y = int(vertical_slider.get())
    send_data(x,y)

def on_submit(btn_name):
    global x,y
    x = int(horizontal_slider.get())
    y = int(vertical_slider.get())

    config_obj[btn_name] = [x,y]

    with open(CFG_FILE_NAME, 'w') as outfile:
        json.dump(config_obj, outfile)

# def save():
#     config_obj['x'] = x
#     config_obj['y'] = y

#     with open(CFG_FILE_NAME, "w") as outfile:
#         json.dump(config_obj, outfile)


# Initialize the main window
root = tk.Tk()
root.title("Calibration")

# Initialize OpenCV webcam
cap = cv2.VideoCapture(0)

# Create a label to display the webcam feed
video_label = tk.Label(root)
video_label.grid(row=0, column=0, padx=10, pady=10)

# Create a horizontal slider
horizontal_slider_label = Label(root, text="Horizontal Slider:")
horizontal_slider_label.grid(row=1, column=0, sticky="ew")

horizontal_slider = Scale(root, from_=180, to=0, orient=tk.HORIZONTAL, command=on_slider_change)
horizontal_slider.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Create a vertical slider
vertical_slider_label = Label(root, text="Vertical Slider:")
vertical_slider_label.grid(row=0, column=1, sticky="ns")

vertical_slider = Scale(root, from_=0, to=180, orient=tk.VERTICAL, command=on_slider_change)
vertical_slider.grid(row=0, column=2, sticky="ns", padx=10, pady=10)

# Create a frame for the buttons in the bottom-right corner
button_frame = Frame(root)
button_frame.grid(row=2, column=2, sticky="se", padx=10, pady=10)

# Create the four buttons
bottom_right_button = Button(button_frame, text="bottom_right", command=lambda: on_submit("bottom_right"))
bottom_right_button.grid(row=1, column=1, padx=5, pady=5)

top_right_button = Button(button_frame, text="top_right", command=lambda: on_submit("top_right"))
top_right_button.grid(row=0, column=1, padx=5, pady=5)

bottom_left_button = Button(button_frame, text="bottom_left", command=lambda: on_submit("bottom_left"))
bottom_left_button.grid(row=1, column=0, padx=5, pady=5)

top_left_button = Button(button_frame, text="top_left", command=lambda: on_submit("top_left"))
top_left_button.grid(row=0, column=0, padx=5, pady=5)

# Start updating the webcam feed
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the webcam when the program exits

# if cv2.waitKey(1) == ord('q'):
cap.release()