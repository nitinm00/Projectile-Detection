import cv2
import time
HORIZ_ASPECT = 640
VERT_ASPECT = 480

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, HORIZ_ASPECT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VERT_ASPECT)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

MS_TO_NS = 1e6
while True:
    start = time.time_ns()
    ret, frame = cap.read()
    print(f'Time to read webcam image:{(time.time_ns() - start) // MS_TO_NS} ms')
    # cv2.imshow('window', frame)

    if cv2.waitKey(1) == ord('q'):
        break