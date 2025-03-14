import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
import imutils

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

def draw_rectangle(frame, tl_x, tl_y, w, h):
    cv2.rectangle(frame, (tl_x , tl_y) , (tl_x+ w, tl_y+h), (0, 255, 0), 2)

def map_to_range(arr, old_min, old_max, new_min, new_max):

    normalized_arr = (arr - old_min)/(old_max - old_min)
    mapped_arr = normalized_arr * (new_max - new_min) + new_min

    return mapped_arr

while True:
    frames = listener.waitForNewFrame()

    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]
    
    registration.apply(color, depth, undistorted, registered,
                       bigdepth=bigdepth,
                       color_depth_map=color_depth_map)
    
    depthimg = depth.asarray() / 4500.
    colorimg = cv2.resize(color.asarray(),
                                   (int(1920 / 3), int(1080 / 3)))
    
    grimg = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)

    #---- Apply automatic Canny edge detection using the computed median----

    depth_8bit = np.array(depthimg * 255., dtype=np.uint8)
    # print(depth_8bit)
    # print("min 8bit:", np.min(depth_8bit))
    # print("max 8bit:", np.max(depth_8bit))
    v = np.median(depth_8bit)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    processed = cv2.medianBlur(depth_8bit, 11)
    processed = cv2.Canny(processed, 5, 70, 3)
    processed = cv2.blur(processed, (7, 7))
    circles = cv2.HoughCircles(processed, cv2.HOUGH_GRADIENT,2,32,
                                param1=30,param2=550,minRadius=0,maxRadius=30)
    # edged_depth = cv2.Canny(depth_8bit, lower, upper)
    # cv2.imshow('Edges',edged_depth)
    cv2.imshow("edges", processed)
    print(circles)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:

            # draw the outer circle
            cv2.circle(colorimg,(i[0],i[1]),i[2],(0,255,0),2)

            # draw the center of the circle
            cv2.circle(colorimg,(i[0],i[1]),2,(0,0,255),3)
        
    cv2.imshow("kinect depth", depthimg)
    cv2.imshow("Kinect webcam", colorimg)

    listener.release(frames)
    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break