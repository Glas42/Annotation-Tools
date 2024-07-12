import cv2
import os

if not os.path.exists(f"{os.path.dirname(__file__)}/Dataset"):
    os.mkdir(f"{os.path.dirname(__file__)}/Dataset")

for file in os.listdir(f"{os.path.dirname(__file__)}/Dataset"):
    img = None
    img = cv2.imread(f"{os.path.dirname(__file__)}/Dataset/{file}")
    if img is None:
        os.remove(f"{os.path.dirname(__file__)}/Dataset/{file}")
    elif img.shape[2] == 3:
        cv2.imwrite(f"{os.path.dirname(__file__)}/Dataset/{file}", cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))