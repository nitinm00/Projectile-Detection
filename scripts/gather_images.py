import cv2 
import os
import glob 
import time 
import argparse

# gather images from the webcam and save them 

parser = argparse.ArgumentParser()

parser.add_argument('filepath', default='gathered_images')
parser.add_argument('-ti', '--interval', default=2)
parser.add_argument('-v', '--verbose', 
                    action='store_true', default=True)

args = parser.parse_args()

folder = args.filepath
v = args.verbose
interval = args.interval

if not os.path.isdir(folder):
    os.mkdir(folder)

files_w_extension = map(os.path.basename, glob.glob(folder + '/*jpg'))
filenames = [os.path.splitext(x)[0] for x in list(files_w_extension)]
num_of_imgs = len(list(map(int, filenames)))

if num_of_imgs > 0:
    frame_count = max(list(map(int, filenames))) 
else: 
    frame_count = 0

print(frame_count)

HORIZ_ASPECT = 640
VERT_ASPECT = 480

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, HORIZ_ASPECT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VERT_ASPECT)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

time.sleep(5)

while True:
    ret, frame = cap.read()

    fn = os.path.join(folder, '%d.jpg' % frame_count)
    cv2.imwrite(fn, frame)
    time.sleep(interval)

    if args.verbose:
        print("photo captured:", fn)

    frame_count += 1
    if cv2.waitKey(1) == ord('q'):
        break