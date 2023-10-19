import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from matplotlib import pyplot as plt

def gamma_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth, 0)
    h, w, = img.shape
    img = cv2.resize(img, (w//3, h//3))
    r = 1.03
    nim = np.power(img, r)
    nim[nim > 255] = 255
    img = np.concatenate([img, nim], axis = 1)
    cv2.imwrite(os.path.join(filepath, r'gamma.jpg'), img)

if __name__ == "__main__":
    gamma_image()