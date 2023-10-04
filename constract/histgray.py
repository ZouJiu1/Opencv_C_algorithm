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
    img = cv2.imread(pth, -1)
    h, w, c = img.shape
    count = np.zeros(256)
    for i in range(h):
        for j in range(w):
            count[img[i, j]] += 1
    plt.plot(range(len(count)), count)
    plt.show()
    plt.close()
    # cv2.imwrite(os.path.join(filepath, r'sunoray_perspective.jpg'), perspectimg)

if __name__ == "__main__":
    histgray_image()