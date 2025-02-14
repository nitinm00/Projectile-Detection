from ultralytics import YOLO

version = 4

DATA_YAML = '/home/nitin/Projects/Projectile Detection/datasets/projectiledetection-%d/data.yaml' % version
MODEL_RESUME_PATH = 'runs/detect/train10/weights/best.pt'

# model = YOLO("../trained-models/yolov11_custom/yolo11s.yaml") # build a new model from YAML
model = YOLO("yolo11s.yaml") # build a new model from YAML

# model = YOLO(MODEL_RESUME_PATH)
# model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)
# model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model

results = model.train(data=DATA_YAML, epochs=30, device='0')

