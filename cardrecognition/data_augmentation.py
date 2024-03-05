import os
import glob
import Augmentor


def augment_images_in_folder(folder_path, target_count=50):
    p = Augmentor.Pipeline(folder_path, output_directory=folder_path)

    existing_images = glob.glob(os.path.join(folder_path, '*'))

    remaining_count = target_count - len(existing_images)

    if remaining_count > 0:
        p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
        p.flip_left_right(probability=0.1)
        p.zoom_random(probability=0.5, percentage_area=0.8)
        p.flip_top_bottom(probability=0.05)

        p.sample(remaining_count)


def augment_images_in_parent_folder(parent_folder_path, target_count=50):
    # Loop through each folder in the parent folder
    for folder_name in os.listdir(parent_folder_path):
        folder_path = os.path.join(parent_folder_path, folder_name)
        if os.path.isdir(folder_path):
            print("Augmenting images in folder:", folder_name)
            augment_images_in_folder(folder_path, target_count)


augment_images_in_parent_folder('C:/Users/user/Desktop/POKEMON_PROJECT/data&model/pkm-data/files/images', target_count=50)
