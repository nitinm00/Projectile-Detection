import cv2 
import os
import glob 
import time 

folder = 'webcam_images'
# folder = os.path.join(os.getcwd(), 'webcam_images')

files_w_extension = map(os.path.basename, glob.glob(folder + '/*jpg'))

filenames = [os.path.splitext(x)[0] for x in list(files_w_extension)]

frame_count = max(list(map(int, filenames)))

print(frame_count)

# frame_count = int(latest_file.split("/")[-1][:3]) + 1
# print(frame_count)

cap = cv2.VideoCapture(0)

time.sleep(5)

while True:
    ret, frame = cap.read()
    cv2.imshow('window', frame)

    cv2.imwrite(os.path.join(folder, '%d.jpg' % frame_count), frame)
    frame_count += 1
    
    if cv2.waitKey(1) == ord('q'):
        break