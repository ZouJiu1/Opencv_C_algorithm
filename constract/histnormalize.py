import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from matplotlib import pyplot as plt

def histgray_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth, 0)
    h, w, = img.shape
    img = cv2.resize(img, (w//3, h//3))
    Imin = np.min(img, )
    Imax = np.max(img, )
    Omin = 100
    Omax = 255
    nim = ((img - Imin) / (Imax - Imin) ) * (Omax - Omin) + Omin
    # nim = cv2.normalize(img, nim, 155, 100, cv2.NORM_MINMAX, -1)
    img = np.concatenate([img, nim], axis = 1)
    cv2.imwrite(os.path.join(filepath, r'histnormalize.jpg'), img)

if __name__ == "__main__":
    histgray_image()