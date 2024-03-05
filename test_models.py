from ultralytics import YOLO
from PIL import Image

import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = YOLO('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/runs/detect/train8/weights/best.onnx')

# Run batched inference on a list of images
results = model(['C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/files/test_images/img.jpg'], conf=0.93)

original_img = Image.open('C:/Users/user/Downloads/20240305_000355.jpg')

cropped_images = []

for result in results:
    boxes = result.boxes

    for box in boxes.xyxy:
        x1, y1, x2, y2 = map(int, box[:4])
        cropped_img = original_img.crop((x1, y1, x2, y2))
        cropped_images.append(np.array(cropped_img))


model = load_model('cardrecognition/pokemon_card_recognition_model_16.keras')

for image in cropped_images:
    img_array = np.expand_dims(image, axis=0)

    img_array = img_array / 255.

    predictions = model.predict(img_array)

    class_indices = {i: folder for i, folder in
                     enumerate(os.listdir('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/files/images'))}

    top_k = 5
    top_indices = np.argsort(predictions[0])[::-1][:top_k]
    top_labels = [class_indices[i] for i in top_indices]
    top_probabilities = predictions[0][top_indices]

    print("Top 5 predicted class labels:")
    for label, prob in zip(top_labels, top_probabilities):
        print(label, ":", prob)
