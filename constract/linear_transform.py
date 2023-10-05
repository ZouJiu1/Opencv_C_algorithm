import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from copy import deepcopy

def lt_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth, -1)
    h, w, c = img.shape
    img = cv2.resize(img, (w//3, h//3))
    
    img0 = 2.0 * deepcopy(img)  # 提升了对比度
    img0[img0 > 255] = 255
    
    img1 = 0.5 * deepcopy(img)  # 降低了对比度

    img2 = deepcopy(img)[...] + [60, 60, 60]  # 提升了亮度
    img2[img2 > 255] = 255

    img3 = deepcopy(img)[...] - [60, 60, 60]  # 降低了亮度
    img3[img3 < 0] = 0

    img = np.concatenate([img, img0, img1, img2, img3], axis = 1)
    cv2.imwrite(os.path.join(filepath, r'linear_transform_sunoray.jpg'), img)

if __name__ == "__main__":
    lt_image()