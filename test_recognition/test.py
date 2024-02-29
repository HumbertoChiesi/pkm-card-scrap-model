from ultralytics import YOLO

model = YOLO('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/runs/detect/train8/weights/best.pt')

# Run batched inference on a list of images
results = model(['C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/files/test_images/img.jpg'], conf=0.93)

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs

    print(boxes)

    probs = result.probs  # Probs object for classification outputs
    result.show()  # display to screen
    result.save(filename='result_08.jpg')  # save to disk
