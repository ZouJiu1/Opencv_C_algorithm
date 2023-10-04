import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np

def scale_image_up():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    scale_ratio = 2
    
    color = [255, 0, 0]
    scaleimg = np.zeros((h * scale_ratio, w * scale_ratio, 2 + 1))
    scaleimg[:, :, :] = color
    
    for i in range(h):
        for j in range(w):
            scaleimg[i * scale_ratio, j*scale_ratio, :] = img[i, j, :]
    # cv2.imshow('origin', img)
    # cv2.imshow('x-60', moveimg)
    # cv2.waitKey(0)
    cv2.imwrite(os.path.join(filepath, r'sunoray_scale%s.jpg'%str(scale_ratio)), scaleimg)

def scale_down_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    scale_ratio = 1/2
    
    color = [255, 0, 0]
    nh, nw = int(h * scale_ratio), int(w * scale_ratio)
    scaleimg = np.zeros((nh, nw, 2 + 1))
    scaleimg[:, :, :] = color
    
    for i in range(h):
        for j in range(w):
            yc = i * scale_ratio
            xc = j * scale_ratio
            if (xc - int(xc)) > 1e-6 or (yc - int(yc)) > 1e-6 or int(xc) >= nw or int(yc) >= nh:
                continue
            scaleimg[int(yc), int(xc), :] = img[i, j, :]
    cv2.imwrite(os.path.join(filepath, r'sunoray_scale%s.jpg'%str(scale_ratio)), scaleimg)

def scale_x0y0_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    scale_ratio = 1/2
    
    color = [255, 0, 0]
    nh, nw = int(h * scale_ratio), int(w * scale_ratio)
    scaleimg = np.zeros((nh, nw, 2 + 1))
    scaleimg[:, :, :] = color
    x0, y0 = 300, 200
    
    for i in range(h):
        for j in range(w):
            yc = y0 + (i - y0) * scale_ratio
            xc = x0 + (j - x0) * scale_ratio
            if (xc - int(xc)) > 1e-6 or (yc - int(yc)) > 1e-6 or int(xc) >= nw or int(yc) >= nh:
                continue
            scaleimg[int(yc), int(xc), :] = img[i, j, :]
    cv2.imwrite(os.path.join(filepath, r'sunoray_x0y0%s.jpg'%str(scale_ratio)), scaleimg)

if __name__ == "__main__":
    scale_image_up()
    scale_down_image()
    scale_x0y0_image()