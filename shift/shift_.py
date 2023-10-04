import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np

def shift_image():
    kk = cv2.__version__
    pth = os.path.join(filepath, r'sunoray.png')
    img = cv2.imread(pth)
    moveimg = np.zeros_like(img)
    h, w, c = img.shape
    
    color = [255, 0, 0]
    x_shift = -100
    ## x-axis -100 shift
    for i in range(h):
        for j in range(w):
            nj = j + x_shift
            if nj < 0:
                moveimg[i, w + nj, :] = color
            elif nj >= w:
                moveimg[i, nj - w, :] = color
            else:
                moveimg[i, nj, :] = img[i, j, :]
    # cv2.imshow('origin', img)
    # cv2.imshow('x-60', moveimg)
    # cv2.waitKey(0)
    concat = np.concatenate([img, moveimg], axis = 0)
    cv2.imwrite(os.path.join(filepath, r'sunoray_x%s_concat.jpg'%str(x_shift)), concat)
    
    ## y-axis +60 shift
    y_shift = +60
    moveimg = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            ni = i + y_shift
            if ni >= h:
                moveimg[ni - h, j, :] = color
            elif ni < 0:
                moveimg[h + ni, j, :] = color
            else:
                moveimg[ni, j, :] = img[i, j, :]
    concat = np.concatenate([img, moveimg], axis = 0)
    cv2.imwrite(os.path.join(filepath, r'sunoray_y%s_concat.jpg'%y_shift), concat)

def shift_image_method2():
    pth = os.path.join(filepath, r'sunoray.png')
    img = cv2.imread(pth)
    moveimg = np.zeros_like(img)
    h, w, c = img.shape
    
    color = [255, 0, 0]
    x_shift = -100
    ## x-axis -100 shift
    if x_shift < 0:   # left
        moveimg[:, w + x_shift:, :] = color
    else: # right
        moveimg[:, :x_shift, :] = color 
    for i in range(h):
        for j in range(w):
            nj = j + x_shift
            if nj < 0 or nj >= w:
                pass
            else:
                moveimg[i, nj, :] = img[i, j, :]
    # cv2.imshow('origin', img)
    # cv2.imshow('x-60', moveimg)
    # cv2.waitKey(0)
    concat = np.concatenate([img, moveimg], axis = 0)
    cv2.imwrite(os.path.join(filepath, r'sunoray_x%s_concat.jpg'%str(x_shift)), concat)
    
    ## y-axis +60 shift
    y_shift = +60
    moveimg = np.zeros_like(img)
    if y_shift < 0:   # up
        moveimg[h + y_shift:, :, :] = color
    else: # down
        moveimg[: y_shift, :, :] = color 
    for i in range(h):
        for j in range(w):
            ni = i + y_shift
            if ni >= h or ni < 0:
                pass
            else:
                moveimg[ni, j, :] = img[i, j, :]
    concat = np.concatenate([img, moveimg], axis = 0)
    cv2.imwrite(os.path.join(filepath, r'sunoray_y%s_concat.jpg'%y_shift), concat)
    
if __name__ == "__main__":
    shift_image()
    shift_image_method2()

# def resize():
#     pth = r'C:\Users\10696\Pictures\v2-6fdf4d3e007a9057872f863147e33a5d_1440w_____.jpg'
#     img = cv2.imread(pth)
#     img = cv2.resize(img, (1600-300, 300))
#     cv2.imwrite(pth.replace(".jpg", ".png"), img)