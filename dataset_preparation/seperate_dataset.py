# Usage: python seperate_dataset.py "source_folder" "image_folder" "txt_folder"
# Contributor: Büşra Yıldırım, Doğa Oytaç

import os
import shutil
import argparse

def main():
    # Command line parser
    parser = argparse.ArgumentParser(description="Seperate text and image files.")
    parser.add_argument("source_folder", type=str, help="The path of source folder.")
    parser.add_argument("image_folder", type=str, help="The path of images folder.")
    parser.add_argument("txt_folder", type=str, help="The path of texts folder.")

    args = parser.parse_args()
    source_folder = args.source_folder
    image_folder = args.image_folder
    txt_folder = args.txt_folder

    # Create image and label folders
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)

    # Seperate folders
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)

        if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg"):
            shutil.move(source_file, image_folder)
        elif file_name.endswith(".txt"):
            shutil.move(source_file, txt_folder)

if __name__ == "__main__":
    main()
    print("Images and labels are succesfully separated.")

 
