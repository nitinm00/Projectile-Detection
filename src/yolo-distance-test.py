# import matplotlib.pyplot as plt
import cv2
import time
from ultralytics import YOLO
import numpy as np
import os
import pickle
from get_trajectory import Trajectory

# model = YOLO('../trained-models/yolov11/yolo11n.pt')
# model = YOLO('../scripts/yolo11n.pt')

VERSION = 12
MODEL_PATH = '/home/nitin/Projects/Projectile Detection/runs/detect/train%d/weights/best.pt' % VERSION
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

S_TO_NS = 1e9 # convert seconds to nanoseconds

# since we are using one camera, we need to know the physical dimensions of the object/projectile
# we're using a ball since it's an object that appears the same size from all perspectives (i.e. a sphere)

# if the object isn't we would have to provide its dimensions along each projection axis 
# and calibrate it as such, which is more difficult

ball_diameter = 0.070 # 7 cm
ball_radius = ball_diameter / 2

# camera intrinsic matrix (from 3d calibration)
# this defines the physical properties of the camera lens, i.e. focal length in x and y, 
K = np.array([[674.81413795,   0,         339.55412501], 
              [  0,         680.6589148,  261.00844856], 
              [  0,           0,           1          ]])
dist = np.array([ 0.15886002,  0.71818958,  0.04643461, -0.00727126, -2.95783407])

f_x = K[0,0]
f_y = K[1,1]

def get_coordinates(ball_center, ball_pixel_width):
    u, v = ball_center
    Z = (f_x * ball_diameter) / ball_pixel_width
    X = (u - K[0,2]) * Z / f_x
    Y = (v - K[1,2]) * Z / f_y
    print(f"3D Position (X, Y, Z): ({X:.2f}, {Y:.2f}, {Z:.2f}) meters")
    return [X, Z, Y]

def undistort_coordiates(coords):
    undistorted = cv2.undistortPoints(coords, cameraMatrix=K, distCoeffs=dist, P=K)
    undist = undistorted[0][0]
    return undist

start = time.time()
traj = Trajectory()

data = []

while True:

    if time.time() - start > 10:
        break

    ret, frame = cap.read()

    results = model(frame, verbose=False)

    single_detection = False

    for result in results:

        if len(result.boxes) == 1:
            
            single_detection = True
        
        if single_detection:

            # get normalized xyxy of bounding rectangle
            
            topleft_x_norm, topleft_y_norm, bottomright_x_norm, bottomright_y_norm = result.boxes[0].xyxyn[0].tolist()

            # scale normalized values by actual image dimensions

            tl_x, br_x = int(topleft_x_norm * HORIZ_ASPECT), int(bottomright_x_norm * HORIZ_ASPECT)
            tl_y, br_y = int(topleft_y_norm * VERT_ASPECT), int(bottomright_y_norm * VERT_ASPECT)
            
            cv2.rectangle(frame, (tl_x, tl_y) , (br_x, br_y), (0, 255, 0), 2)

            ball_pixel_width = ( (br_x - tl_x) + (br_y - tl_y) ) / 2

            distorted_ball_center = np.array([ (tl_x + (br_x - tl_x) / 2), (tl_y + (br_y - tl_y) / 2) ])

            # undistort the detected point
            undist = undistort_coordiates(distorted_ball_center)

            # compute x, y, z using known ball dimensions, its pixel width in image, 
            # target coordinates, and camera x, y focal length 
            # note that X,Y plane is the projection plane, and Z is depth away from camera 
            
            # give each point a timestamp to determine velocity 
            data.append([time.time_ns(), get_coordinates(undist, ball_pixel_width)])

            print([time.time_ns(), get_coordinates(undist, ball_pixel_width)])
            
            if len(data) == 5:

                # get two data points with longest time interval between them since that will be
                # the bottleneck and give the most accurate time

                ints = [data[i][0]-data[i-1][0] for i in range(5)]
                ts = max(ints)
                interval = ints.index(ts)

                position_in_1s = traj.predict_position([data[interval][1], data[interval+1][1]], data[len(data)-1] + (1 * S_TO_NS), ts)

                print("position in 1 sec", position_in_1s)
            

    # print("next image")
    cv2.imshow("Webcam",frame)

    # time.sleep(1)
    if cv2.waitKey(1) == ord('q'):
        break

# print(data)

# if not os.path.exists('trajectory-data'):
#     os.create
# with open('trajectory-data', 'ab') as outfile:
    # pickle.dumps(data, outfile)

with open('trajectory-data', 'w') as outfile:
    outfile.write(str(data))

# data = np.array(data)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot(data[0], data[1], data[2], label="ball trajectory", color="blue", marker="o", markersize=3)

# plt.show()