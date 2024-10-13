# Usage: python set_classes.py "folder"
# Contributor: Doğa Oytaç

import os
import argparse

parser = argparse.ArgumentParser(description="Modify class id's.")
parser.add_argument("folder", type=str, help="The path of source folder.")

args = parser.parse_args()
folder = args.folder

def change_text_file(file_path):

    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        class_id =  line[0]

        if class_id == "1":
            new_line = "0" + line[1:]
        elif class_id == "0":
            new_line = "1" + line[1:]
        new_lines.append(new_line)
    
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":

    folder_name = os.path.basename(folder)

    os.chdir(folder)

    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = os.path.join(folder, file)
            print(file_path)
            change_text_file(file_path)

