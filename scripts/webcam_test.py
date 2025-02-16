import cv2

HORIZ_ASPECT = 640
VERT_ASPECT = 480

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, HORIZ_ASPECT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VERT_ASPECT)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

while True:
    ret, frame = cap.read()

    cv2.imshow('window', frame)

    if cv2.waitKey(1) == ord('q'):
        break