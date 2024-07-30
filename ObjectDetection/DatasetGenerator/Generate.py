import numpy as np
import random
import cv2
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
(images_train, labels_train), (images_test, labels_test) = tf.keras.datasets.mnist.load_data()

save_path = os.path.dirname(__file__) + "/Dataset"
save_path = save_path[:-1] if save_path[-1] in ["/", "\\"] else save_path

if not os.path.exists(save_path):
    os.mkdir(save_path)

exit() if not os.path.exists(save_path) else None

number_of_images_to_generate = -1
while number_of_images_to_generate < 0:
    number_of_images_to_generate_input = input("How many images do you want to generate?\n-> ")
    try:
        number_of_images_to_generate = int(number_of_images_to_generate_input)
    except:
        number_of_images_to_generate = -1

image_size = []
while len(image_size) != 2 or image_size[0] > image_size[1]:
    image_size = input("How big should the image be? (min, max)\n-> ").split(",")
    try:
        image_size = [int(x.strip()) for x in image_size]
    except:
        image_size = []
image_size = {"low": image_size[0], "high": image_size[1]}

number_of_digits_per_image = []
while len(number_of_digits_per_image) != 2 or number_of_digits_per_image[0] > number_of_digits_per_image[1]:
    number_of_digits_per_image = input("How many digits should be in each image? (min, max)\n-> ").split(",")
    try:
        number_of_digits_per_image = [int(x.strip()) for x in number_of_digits_per_image]
    except:
        number_of_digits_per_image = []
number_of_digits_per_image = {"low": number_of_digits_per_image[0], "high": number_of_digits_per_image[1]}

save_format = None
while save_format is None:
    save_format_input = input("Which format would you like to use for the labels? (1: (label,x1,y1,x2,y2), 2: (label cx cy w h))\n-> ")
    try:
        save_format = int(save_format_input)
        if save_format not in [1, 2]:
            save_format = None
    except ValueError:
        save_format = None

exit() if input(f'Are you sure you want to generate {number_of_images_to_generate} images in the "{save_path}" folder? (y/n)\n-> ').lower() != "y" else None

for _ in range(number_of_images_to_generate):
    image_width = random.randint(image_size["low"], image_size["high"])
    image_height = random.randint(image_size["low"], image_size["high"])
    frame = np.zeros((image_height, image_width), dtype=np.uint8)
    annotation = []
    for i in range(random.randint(number_of_digits_per_image["low"], number_of_digits_per_image["high"])):
        digit_placed = False
        while not digit_placed:
            x = np.random.randint(0, (image_width - 29))
            y = np.random.randint(0, (image_height - 29))
            index = np.random.randint(0, len(images_train))
            digit = images_train[index]
            label = labels_train[index]
            if np.sum(frame[y:(y+28), x:(x+28)]) == 0:
                min_x, min_y, max_x, max_y = float("inf"), float("inf"), 0, 0
                for row in range(28):
                    for col in range(28):
                        if digit[row][col] != 0:
                            if col < min_x:
                                min_x = col
                            if col > max_x:
                                max_x = col
                            if row < min_y:
                                min_y = row
                            if row > max_y:
                                max_y = row
                min_x += x
                min_y += y
                max_x += x
                max_y += y
                min_x /= frame.shape[1]
                min_y /= frame.shape[0]
                max_x /= frame.shape[1]
                max_y /= frame.shape[0]
                if save_format == 1:
                    annotation.append(f"{label},{min_x},{min_y},{max_x},{max_y}")
                elif save_format == 2:
                    cx = (min_x + max_x) / 2
                    cy = (min_y + max_y) / 2
                    w = max_x - min_x
                    h = max_y - min_y
                    annotation.append(f"{label} {cx} {cy} {w} {h}")
                frame[y:(y+28), x:(x+28)] = digit
                digit_placed = True

    name = len(os.listdir(save_path)) // 2

    with open(f"{save_path}/{name}.txt", "w") as f:
        f.write("\n".join(annotation))
        f.close()

    cv2.imwrite(f"{save_path}/{name}.png", frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    for box in annotation:
        _, cx, cy, w, h = box.split(" ")
        x1 = round((float(cx) - float(w) / 2) * frame.shape[1])
        y1 = round((float(cy) - float(h) / 2) * frame.shape[0])
        x2 = round((float(cx) + float(w) / 2) * frame.shape[1])
        y2 = round((float(cy) + float(h) / 2) * frame.shape[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imshow("MNIST Grid", frame)
    cv2.waitKey(1)