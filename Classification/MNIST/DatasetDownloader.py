import os
import cv2
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

PATH = os.path.dirname(__file__) + "\\"

clear = input("Do you want to clear the dataset folder before downloading? (y/n)\n-> ").lower() == "y"

print("\nLoading...")

import tensorflow as tf
(images_train, labels_train), (images_test, labels_test) = tf.keras.datasets.mnist.load_data()

train_image_dir = f"{PATH}Dataset/train_images"
train_label_dir = f"{PATH}Dataset/train_labels"
test_image_dir = f"{PATH}Dataset/test_images"
test_label_dir = f"{PATH}Dataset/test_labels"

if os.path.exists(train_image_dir) == False:
    os.mkdir(train_image_dir)
if os.path.exists(train_label_dir) == False:
    os.mkdir(train_label_dir)
if os.path.exists(test_image_dir) == False:
    os.mkdir(test_image_dir)
if os.path.exists(test_label_dir) == False:
    os.mkdir(test_label_dir)

if clear:
    for file in os.listdir(train_image_dir):
        try:
            os.remove(os.path.join(train_image_dir, file))
        except:
            pass
    for file in os.listdir(train_label_dir):
        try:
            os.remove(os.path.join(train_label_dir, file))
        except:
            pass
    for file in os.listdir(test_image_dir):
        try:
            os.remove(os.path.join(test_image_dir, file))
        except:
            pass
    for file in os.listdir(test_label_dir):
        try:
            os.remove(os.path.join(test_label_dir, file))
        except:
            pass

os.makedirs(f"{PATH}dataset", exist_ok=True)
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(test_image_dir, exist_ok=True)
os.makedirs(test_label_dir, exist_ok=True)

print(f"\rCopying train images and labels...", end="", flush=True)
for i, (image, label) in enumerate(zip(images_train, labels_train)):
    if f"{i}.png" in os.listdir(train_image_dir) and f"{i}.txt" in os.listdir(train_label_dir):
        continue
    image_path = os.path.join(train_image_dir, f"{len(os.listdir(train_image_dir))}.png")
    label_path = os.path.join(train_label_dir, f"{len(os.listdir(train_label_dir))}.txt")
    cv2.imwrite(image_path, image)
    with open(label_path, 'w') as f:
        f.write(str(label))
    if i % 100 == 0:
        print(f"\rCopying train images and labels ({round(i / len(images_train) * 100)}%)", end="", flush=True)

print(f"\rCopying test images and labels...", end="", flush=True)
for i, (image, label) in enumerate(zip(images_test, labels_test)):
    if f"{i}.png" in os.listdir(test_image_dir) and f"{i}.txt" in os.listdir(test_label_dir):
        continue
    image_path = os.path.join(test_image_dir, f"{len(os.listdir(test_image_dir))}.png")
    label_path = os.path.join(test_label_dir, f"{len(os.listdir(test_label_dir))}.txt")
    cv2.imwrite(image_path, image)
    with open(label_path, 'w') as f:
        f.write(str(label))
    if i % 100 == 0:
        print(f"\rCopying test images and labels ({round(i / len(images_test) * 100)}%)", end="", flush=True)

print("Done!")