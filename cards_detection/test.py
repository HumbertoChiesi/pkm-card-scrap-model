from ultralytics import YOLO

model = YOLO('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/runs/detect/train8/weights/best.onnx')

results = model(['C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/files/test_images/img.jpg'], conf=0.93)

# Process results list
for result in results:
    boxes = result.boxes

    probs = result.probs
    result.show()
    result.save(filename='../images/result_08.jpg')
