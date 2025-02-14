import roboflow

with open('RF_API_KEY.key', 'r') as openfile:
    API_KEY = openfile.read()

rf = roboflow.Roboflow(api_key=API_KEY)
project = rf.workspace("projectiledetection").project("projectiledetection")

#can specify weights_filename, default is "weights/best.pt"
version = project.version(3)
# version.deploy("model-type", "path/to/training/results/", "weights_filename")

#example1 - directory path is "training1/model1.pt" for yolov8 model
version.deploy("yolov11", "runs/detect/train6")

