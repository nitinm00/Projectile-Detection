import cv2
import time
from ultralytics import YOLO
import numpy as np

# model = YOLO('../trained-models/yolov11/yolo11n.pt')
# model = YOLO('../scripts/yolo11n.pt')

MODEL_PATH = '/home/nitin/Projects/Projectile Detection/scripts/runs/detect/train/weights/best.pt'
model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(0)

HORIZ_ASPECT = 640
VERT_ASPECT = 480
CAM_DIAG_FOV = 78

cap.set(cv2.CAP_PROP_FRAME_WIDTH, HORIZ_ASPECT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VERT_ASPECT)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# w, h = 1920, 1080
# w, h = 640, 480

while True:
    ret, frame = cap.read()

    results = model(frame)
    # print(results)

    for result in results:

        # get normalized xyxy of bounding rectangle

        # for box in result.boxes:
        if len(result.boxes) == 1:
            # print(result.boxes[0].xyxyn)
            
            box = result.boxes[0]
            tensor_list = box.xyxyn[0].tolist()
            
            # print(tensor_np)
            topleft_x_norm, topleft_y_norm, bottomright_x_norm, bottomright_y_norm = box.xyxyn[0].tolist()

            # # scale normalized values by actual image dimensions
            tl_x, br_x = int(topleft_x_norm * HORIZ_ASPECT), int(bottomright_x_norm * HORIZ_ASPECT)

            tl_y, br_y = int(topleft_y_norm * VERT_ASPECT), int(bottomright_y_norm * VERT_ASPECT)

            cv2.rectangle(frame, (tl_x, tl_y) , (br_x, br_y), (0, 255, 0), 2)

    # print("next image")
    cv2.imshow("Webcam",frame)

    # time.sleep(1)
    if cv2.waitKey(1) == ord('q'):
        break

