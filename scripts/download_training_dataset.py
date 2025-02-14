from roboflow import Roboflow

with open('RF_API_KEY.key', 'r') as openfile:
    API_KEY = openfile.read()

rf = Roboflow(api_key=API_KEY)

project = rf.workspace("projectiledetection").project("projectiledetection")
version = project.version(4)
dataset = version.download("yolov11")
