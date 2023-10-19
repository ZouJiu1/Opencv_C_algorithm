import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from matplotlib import pyplot as plt

def equal_histgray_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    # pth = os.path.join(filepath, r'..\an.jpg')
    # pth = os.path.join(filepath, r'..\hunan.jpg')
    img = cv2.imread(pth, 0)
    h, w = img.shape
    # img = cv2.resize(img, (w//4, h//4))
    # h, w = img.shape
    count = np.zeros(256)
    for i in range(h):
        for j in range(w):
            count[img[i, j]] += 1
    cumsum = np.cumsum(count)
    nimg = np.zeros_like(img)
    areas = h * w
    for i in range(h):
        for j in range(w):
            nimg[i, j] = (256 / areas) * cumsum[img[i, j]] - 1
    nimg[nimg > 255] = 255
    nimg[nimg < 0] = 0
    
    countafter = np.zeros(256)
    for i in range(h):
        for j in range(w):
            countafter[nimg[i, j]] += 1
    plt.plot(range(len(countafter)), countafter)
    # plt.plot(range(len(countafter)), np.cumsum(countafter))
    plt.show()
    plt.close()
    img = np.concatenate([img, nimg], axis = 1)
    cv2.imwrite(os.path.join(filepath, r'equalhist.jpg'), img)

if __name__ == "__main__":
    equal_histgray_image()