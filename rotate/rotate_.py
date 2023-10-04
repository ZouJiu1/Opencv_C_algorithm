import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np

def rotate_image():
    kk = cv2.__version__
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    
    ch, cw = h//2, w//2
    
    color = [255, 0, 0]
    angle = np.pi / 3
    rotateimg = np.zeros_like(img)
    rotateimg[...] = color
    
    m1 = np.array([[1, 0, cw], [0, 1, ch], [0, 0, 1]])
    A  = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]]) # 顺时针
    A  = np.array([[np.cos(angle), np.sin(angle), 0], [-np.sin(angle), np.cos(angle), 0], [0, 0, 1]]) # 逆时针
    m2 = np.array([[1, 0, -cw], [0, 1, -ch], [0, 0, 1]])
    for i in range(h):
        for j in range(w):
            p = np.array([j, i, 1]).reshape((-1, 1))
            out = np.matmul(m2, p)
            out = np.matmul(A, out)
            out = np.matmul(m1, out)
            x = int(out[0][0])
            y = int(out[1][0])
            if x < 0 or x >= w or y < 0 or y >= h:
                continue
            rotateimg[y, x, :] = img[i, j, :]

    cv2.imwrite(os.path.join(filepath, r'sunoray_rotate%s.jpg'%str(angle)), rotateimg)

if __name__ == "__main__":
    rotate_image()