from roboflow import Roboflow
import os

with open('RF_API_KEY.key', 'r') as openfile:
    API_KEY = openfile.read()

rf = Roboflow(api_key=API_KEY)

project = rf.workspace("projectiledetection").project("projectiledetection")
# version = project.version(1)

folder = 'webcam_images'
files_w_extension = [os.path.join(folder, filepath) for filepath in os.listdir(folder)]
# print(files_w_extension)

for file in files_w_extension:
    project.upload(file)