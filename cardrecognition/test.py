import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model('pokemon_card_recognition_model.h5')

image_path = 'C:/Users/user/Downloads/image.webp'

img = image.load_img(image_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to match the batch size

img_array = img_array / 255.

predictions = model.predict(img_array)

class_indices = {i: folder for i, folder in enumerate(os.listdir('C:/Users/user/Desktop/pkm-site/files/images'))}

top_k = 5
top_indices = np.argsort(predictions[0])[::-1][:top_k]
top_labels = [class_indices[i] for i in top_indices]
top_probabilities = predictions[0][top_indices]

print("Top 5 predicted class labels:")
for label, prob in zip(top_labels, top_probabilities):
    print(label, ":", prob)