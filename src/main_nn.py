import cv2
import numpy as np
import imutils

import serial
import time
import platform

from ultralytics import YOLO

object_h_thresh = 0.1
object_w_thresh = 0.1
MS_TO_NS = 1e6

HORIZ_ASPECT = 640
VERT_ASPECT = 480
CAM_DIAG_FOV = 78

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, HORIZ_ASPECT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VERT_ASPECT)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

DIAG_ASPECT = np.sqrt(HORIZ_ASPECT**2 + VERT_ASPECT**2)

HORIZ_FOV = 2 * np.arctan( np.tan( np.deg2rad(CAM_DIAG_FOV/2) * HORIZ_ASPECT/DIAG_ASPECT))
VERT_FOV = 2 * np.arctan ( np.tan( np.deg2rad(CAM_DIAG_FOV/2) * VERT_ASPECT/DIAG_ASPECT))

H_SCALING_FACTOR = HORIZ_FOV/180
V_SCALING_FACTOR = VERT_FOV/180

plat = platform.system()

if plat == "Windows":
    port = "COM4"
elif plat == "macOS":
    # port = "/dev/tty.usbmodem6D8118A649481"
    port = "/dev/tty.usbmodem144101"
elif plat == "Linux":
    port = "/dev/ttyUSB0"

VERSION = 12
MODEL_PATH = '/home/nitin/Projects/Projectile Detection/runs/detect/train%d/weights/best.pt' % VERSION
model = YOLO(MODEL_PATH)

out = serial.Serial(port, baudrate=9600, timeout=1)

start = time.time_ns()

if not cap.isOpened():
    print("could not open camera")

# may need to flip orientation of controls depending on the orientation of the servos
def flip_orientation(x):
    return 180 - x

def send_data(x, y):
        # start = time.time_ns()
        global start
        if (time.time_ns() - start) > (15 * MS_TO_NS):
            out.write(b'X%dY%d\n' %(x,y))   
            start = time.time_ns()

def target(tl_x, tl_y, br_x, br_y):

    cx = tl_x + (br_x - tl_x)/2
    cy = tl_y + (br_y - tl_y)/2

    X =  flip_orientation((cx/HORIZ_ASPECT)*180)
    Y =  (cy/VERT_ASPECT)*180

    send_data(X, Y)
    # print(X,Y)
    
while True:
    ret, frame = cap.read()

    if not ret:
        print("could not read frame")
        break

    # results = model(frame, device='0', verbose=False)
    results = model(frame, device='0', verbose=True)

    for result in results:

        # get normalized xyxy of bounding rectangle

        if len(result.boxes) == 1:
            
            box = result.boxes[0]
            
            topleft_x_norm, topleft_y_norm, bottomright_x_norm, bottomright_y_norm = box.xyxyn[0].tolist()

            # scale normalized values by actual image dimensions
            tl_x, br_x = int(topleft_x_norm * HORIZ_ASPECT), int(bottomright_x_norm * HORIZ_ASPECT)

            tl_y, br_y = int(topleft_y_norm * VERT_ASPECT), int(bottomright_y_norm * VERT_ASPECT)

            cv2.rectangle(frame, (tl_x, tl_y) , (br_x, br_y), (0, 255, 0), 2)

            target(tl_x, tl_y, br_x, br_y)

    cv2.imshow("Webcam",frame)

    if cv2.waitKey(1) == ord('q'):
        break
