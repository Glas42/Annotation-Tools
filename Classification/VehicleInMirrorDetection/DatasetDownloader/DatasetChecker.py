import cv2
import os

if not os.path.exists(f"{os.path.dirname(__file__)}/Dataset"):
    os.mkdir(f"{os.path.dirname(__file__)}/Dataset")

aspect_ratio = 288 / 261

for file in os.listdir(f"{os.path.dirname(__file__)}/Dataset"):
    img = None
    img = cv2.imread(f"{os.path.dirname(__file__)}/Dataset/{file}")
    if img is None:
        os.remove(f"{os.path.dirname(__file__)}/Dataset/{file}")
    elif abs(img.shape[1] / img.shape[0] - aspect_ratio) < 0.15:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        os.remove(f"{os.path.dirname(__file__)}/Dataset/{file}")