import numpy as np
import cv2 as cv
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
import imutils
from time import sleep

try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)

# Create and set logger
logger = createConsoleLogger(LoggerLevel.Debug)
setGlobalLogger(logger)

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

listener = SyncMultiFrameListener(
    FrameType.Color | FrameType.Ir | FrameType.Depth)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

device.start()

# NOTE: must be called after device.start()
registration = Registration(device.getIrCameraParams(),
                            device.getColorCameraParams())

undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)

# Optinal parameters for registration
# set True if you need
need_bigdepth = False
need_color_depth_map = False

bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
color_depth_map = np.zeros((424, 512),  np.int32).ravel() \
    if need_color_depth_map else None

COLOR_SIZE = [1920/3, 1080/3]
DEPTH_IR_FRAME_SIZE = [512, 424]

def draw_rectangle(frame, tl_x, tl_y, w, h):
    cv.rectangle(frame, (tl_x , tl_y) , (tl_x+ w, tl_y+h), (0, 255, 0), 2)

def normalize_coordinates_tocolor(x, y):
    return x * int(COLOR_SIZE[0] / DEPTH_IR_FRAME_SIZE[0]), y * int(COLOR_SIZE[1] / DEPTH_IR_FRAME_SIZE[1])

def map_to_range(arr, old_min, old_max, new_min, new_max):

    normalized_arr = (arr - old_min)/(old_max - old_min)
    mapped_arr = normalized_arr * (new_max - new_min) + new_min

    return mapped_arr

def apply_postprocessing(mask):
    
    kernel = np.ones((2, 2), np.uint16)
    
    mask = cv.dilate(mask, kernel, iterations=1)
    mask = cv.erode(mask, kernel,iterations=2) 
    
    return mask

while True:
    frames = listener.waitForNewFrame()

    color_dsize = 2 ** 8
    ir_dsize = 65535.
    depth_dsize = 4500.
    color = frames["color"].asarray()
    ir = frames["ir"].asarray()
    depth = frames["depth"].asarray()
    
    # registration.apply(color, depth, undistorted, registered,
    #                    bigdepth=bigdepth,
    #                    color_depth_map=color_depth_map)
    
    # depthimg = depth / 4500.
    # colorimg = cv2.resize(color,
    #                                (int(1920 / 3), int(1080 / 3)))
    
    ret, thresh = cv.threshold(ir / ir_dsize, 1. - (1 / ir_dsize), 1.0, cv.THRESH_BINARY)
    processed_mask = apply_postprocessing(thresh)
    thresh_8bit = np.array(processed_mask, dtype=np.uint8)
    visible_markers = cv.findContours(thresh_8bit, cv.RETR_LIST,
        cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(visible_markers)
    
    color_frame = cv.resize(color, (int(1920 / 3), int(1080 / 3)))
    contours_poly = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    markers = np.zeros((thresh_8bit.shape[0], thresh_8bit.shape[1], 3), dtype=np.uint8)
    ball = np.zeros((thresh_8bit.shape[0], thresh_8bit.shape[1], 3), dtype=np.uint8)

    if len(contours) > 0:

        # get centers of markers and connect them to form full ball contour
        # or go die and just use average positions of markers
        for i, c in enumerate(contours):
            contours_poly[i] = cv.approxPolyDP(c, 3, True)
            centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
            cv.circle(markers, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color=(0, 255, 0), thickness=2)
        
        # create shape known as "ball"
        if len(centers) > 0:
            print(centers)
            centers = np.array(centers, dtype=np.int32)
            [x, y] = np.average(centers, axis=0)
            avg_dist = np.average(np.array([np.sqrt((xcoord - x) ** 2 + (ycoord - y) ** 2) for (xcoord, ycoord) in centers], np.int32))
            print(f"ball xy rad: {x}, {y}, {avg_dist}")
            cv.circle(ball, (int(x), int(y)), int(avg_dist), (0, 0, 255), 2)

    cv.imshow("thresholded img", processed_mask)
    cv.imshow("markers", markers)
    cv.imshow("ball", ball)

    listener.release(frames)
    key = cv.waitKey(delay=1)
    if key == ord('q'):
        break