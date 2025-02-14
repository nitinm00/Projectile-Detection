import cv2
import time
import platform
import serial

cap = cv2.VideoCapture(0)
plat = platform.system()

if plat == "Windows":
    port = "COM4"
elif plat == "macOS":
    # port = "/dev/tty.usbmodem6D8118A649481"
    port = "/dev/tty.usbmodem144101"
elif plat == "Linux":
    port = "/dev/ttyUSB0"
start = time.time_ns()

out = serial.Serial(port, baudrate=115200, timeout=1)
print(out.name)
ms_to_ns = 1e6
def send_data(x, y):
        # start = time.time_ns()
        global start
        if time.time_ns() - start > 15 * ms_to_ns:
            out.write(b'X%dY%d\n' %(x,y))   
            start = time.time_ns()

# def target(tl_x, tl_y, w, h):
#     # get center
#     cx = tl_x + 0.5 * w
#     cy = tl_y + 0.5 * h

#     # translate to degrees
#     X = h_scaling_factor * (180 - (cx/horiz_aspect)*180)
#     Y = v_scaling_factor * (180 - (cy/vert_aspect)*180)

#     send_data(X, Y)
#     print((tl_x, tl_y, w, h))

while True:
    
    ret, frame = cap.read()
    cv2.imshow("webcam", frame)

    send_data(100, 100)
    if cv2.waitKey(1) == ord('q'):
        break