from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8s.pt')

# Train the model using the 'coco128.yaml' dataset for 3 epochs
results = model.train(data='./project.yaml', epochs=10)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/test_recognition/20230327_143424.jpg')

# Export the model to ONNX format
success = model.export(format='onnx')
