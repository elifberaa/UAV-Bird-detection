# Usage: python data_augmentation.py "<dataset path>" ratio
# Contributor: Doğa Oytaç

import torch
import torchvision
from torchvision.transforms import v2

from imutils import paths
import random
import os
import argparse


class DataAugmentation():
    def __init__(self):
        super().__init__()

    def random_flip(self, image, step):

        flip_direction = random.choice(["vertical", "horizontal", "both"])

        if flip_direction == "vertical":
            flip = v2.RandomVerticalFlip(p=1)
        
        if flip_direction == "horizontal":
            flip = v2.RandomHorizontalFlip(p=1)
        
        if flip_direction == "both":
            flip = v2.Compose([
                v2.RandomVerticalFlip(p=1),
                v2.RandomHorizontalFlip(p=1),
            ])
        
        flipped_img = flip(image)
        pil_img = v2.ToPILImage()
        img = pil_img(flipped_img)

        img.save(f"./new_images/{step}_aug.jpg")

    def crop_image(self, image, step):

        _, __, w, h = image.shape

        if w > 600 or h > 600:

            down_crop = 100
            left_crop = 120

            crop_dim = (0, down_crop, w-left_crop , h - down_crop)

            cropped_img = v2.functional.crop(image, *crop_dim)

            pil_img = v2.ToPILImage()
            img = pil_img(cropped_img.squeeze(0))
            img.save(f"./new_images/{step}_aug.jpg")

    def gaussian_noise(self, image, step):

        transform = v2.Compose([
            v2.GaussianNoise(mean=0.3, sigma=0.15),
            v2.ToPILImage()
        ])

        img = transform(image)
        img.save(f"./new_images/{step}_aug.jpg")

    def color_jitter(self, image, step):

        transform = v2.Compose([
            v2.ColorJitter(brightness=0.5, contrast=1, hue=0.5),
            v2.ToPILImage()
        ])

        img = transform(image)
        img.save(f"./new_images/{step}_aug.jpg")

    def prepare_dataset(self, dataset):

        image_paths = list(paths.list_images(dataset))
        num_subset = int(ratio * len(image_paths))

        if num_subset % 4 != 0:
            num_subset = round(num_subset / 4) * 4

        selected_paths = random.sample(image_paths, num_subset)
        num_per_subset = num_subset // 4

        groups = [selected_paths[i : i + num_per_subset] for i in range(0, len(selected_paths), num_per_subset)]

        return groups


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, help="Folder path of dataset.")
    parser.add_argument("ratio", type=float, help="Ratio of pictures to be augmented.")

    args = parser.parse_args()
    dataset = args.dataset
    ratio = args.ratio 

    augment = DataAugmentation()
    groups = augment.prepare_dataset(dataset)

    os.makedirs("./new_images")

    transform = v2.Compose([
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True)
    ])

    step = 0

    for i, group in enumerate(groups):
    
        for image in group:

            step += 1

            img = torchvision.io.read_image(os.path.join(dataset, image))
            img_tensor = transform(img)

            if i==0:
                augment.random_flip(img_tensor, step)

            elif i==1:
                augment.crop_image(img_tensor.unsqueeze(0), step)

            elif i==2:
                augment.gaussian_noise(img_tensor, step)

            elif i==3:
                augment.color_jitter(img_tensor, step)

