import cv2
import numpy as np
import imutils

import serial
import time
import platform
# import tensorflow_hub as tf_hub

object_h_thresh = 0.1
object_w_thresh = 0.1
ms_to_ns = 1e6

# cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)

plat = platform.system()

# if plat == "Windows":
#     PORT = "COM4"
# elif plat == "macOS":
#     # port = "/dev/tty.usbmodem6D8118A649481"
#     PORT = "/dev/tty.usbmodem144101"
# elif plat == "Linux":
#     PORT = "/dev/ttyUSB0"

# out = serial.Serial(PORT, baudrate=115200, timeout=1)
# print(out.name)

horiz_aspect = 640
vert_aspect = 480
camera_diagonal_FOV = 78

cap.set(cv2.CAP_PROP_FRAME_WIDTH, horiz_aspect)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vert_aspect)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

diagonal_aspect = np.sqrt(horiz_aspect**2 + vert_aspect**2)

horizontal_FOV = 2 * np.arctan( np.tan( np.deg2rad(camera_diagonal_FOV/2) * horiz_aspect/diagonal_aspect))
vertical_FOV = 2 * np.arctan ( np.tan( np.deg2rad(camera_diagonal_FOV/2) * vert_aspect/diagonal_aspect))

h_scaling_factor = horizontal_FOV/180
v_scaling_factor = vertical_FOV/180

masks = {}
masks['red'] = []
masks['green'] = []

lower_red = np.array([140,100,80])
upper_red = np.array([190,255,255])
masks['red'].append([lower_red, upper_red])

lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])
masks['green'].append([lower_green, upper_green])

print(masks)

if not cap.isOpened():
    print("could not open camera")
def apply_postprocessing(mask):
    
    kernel = np.ones((10, 10), np.uint16)
    
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel,iterations=2) 
    
    return mask
    
def get_color_mask(frame, color):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, masks[color][0][0], masks[color][0][1])
        
    return hsv, mask
    
def draw_rectangle(frame, tl_x, tl_y, w, h):
    cv2.rectangle(frame, (tl_x , tl_y) , (tl_x+ w, tl_y+h), (0, 255, 0), 2)

# def send_data(x, y):
#         # start = time.time_ns()
#         global start
#         if time.time_ns() - start > 15 * ms_to_ns:
#             out.write(b'X%dY%d\n' %(x,y))   
#             start = time.time_ns()

# def target(tl_x, tl_y, w, h):
#     # get center
#     cx = tl_x + 0.5 * w
#     cy = tl_y + 0.5 * h

#     # translate to degrees
#     X = h_scaling_factor * (180 - (cx/horiz_aspect)*180)
#     Y = v_scaling_factor * (180 - (cy/vert_aspect)*180)

#     send_data(X, Y)
#     print((tl_x, tl_y, w, h))

start = time.time_ns()

while True:
    ret, frame = cap.read()

    if not ret:
        print("could not read frame")
        break

    # res = cv2.bitwise_and(frame, color_mask(frame))
    blurred = cv2.GaussianBlur(frame, (5, 5), 1)
       
    _, rm = get_color_mask(blurred, 'red')
    
    p = apply_postprocessing(rm)
    
    contours = cv2.findContours(p, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE )
    contours = imutils.grab_contours(contours)
    
    if len(contours) > 0:
        
        ball = max(contours, key=cv2.contourArea)
        
        tl_x, tl_y, w, h = cv2.boundingRect(ball)
        
        # if w > object_w_thresh * f_width and h > object_h_thresh * f_height:
        if w > 20 and h > 20:
            # print(tl_x, tl_y, w, h)
            # print(type(tl_x))
            draw_rectangle(frame, tl_x, tl_y, w, h)
            
            # target(tl_x, tl_y, w, h)

    cv2.imshow("Webcam",frame)

    if cv2.waitKey(1) == ord('q'):
        break
