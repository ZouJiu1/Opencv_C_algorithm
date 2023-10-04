import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np

def get():
    inpoint = np.array([[0, 0], [200, 0], [0, 200], [200, 200]], dtype=np.float32)
    outpoint = np.array([[100, 20], [200, 20], [60, 60], [260, 60]], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(inpoint, outpoint)
    return matrix

def perspective_image():
    kk = cv2.__version__
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    
    color = [255, 0, 0]
    perspectimg = np.zeros_like(img)
    perspectimg[...] = color

    inpoint = np.array([[0, 0], [w - 1, 0], [0, h-1], [w-1, h-1]], dtype=np.float32)
    outpoint = np.array([[100, 100], [w - 20, 20], [60, h - 100], [w-100, h - 60]], dtype=np.float32)
    A = cv2.getPerspectiveTransform(inpoint, outpoint)
    
    # perspectimg = cv2.warpPerspective(img, A, (w, h))

    for i in range(h):
        for j in range(w):
            p = np.array([j, i, 1]).reshape((-1, 1))
            out = np.matmul(A, p)
            x = int(out[0][0])
            y = int(out[1][0])
            if x < 0 or x >= w or y < 0 or y >= h:
                continue
            perspectimg[y, x, :] = img[i, j, :]

    cv2.imwrite(os.path.join(filepath, r'sunoray_perspective.jpg'), perspectimg)

if __name__ == "__main__":
    get()
    perspective_image()