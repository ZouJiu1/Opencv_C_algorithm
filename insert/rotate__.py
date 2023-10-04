import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from neighbor_insert import LINEARinsert, NEARESTinsert

def rotate_image():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    
    ch, cw = h//2, w//2
    
    color = [255, 0, 0]
    angle = np.pi / 3
    rotateimg = np.zeros_like(img)
    rotateimg[...] = color
    '''
顺时针还是逆时针，主要是极坐标的正方向是 顺时针，所以角度是正号，若是逆时针，此时就是极坐标的反方向，需要加上负号才可以
    '''
    m1 = np.array([[1, 0, cw], [0, 1, ch], [0, 0, 1]])
    A  = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]]) # 顺时针
    A  = np.array([[np.cos(angle), np.sin(angle), 0], [-np.sin(angle), np.cos(angle), 0], [0, 0, 1]]) # 逆时针
    m2 = np.array([[1, 0, -cw], [0, 1, -ch], [0, 0, 1]])
    
    Amatrix = np.matmul(np.matmul(m1, A), m2)
    Ainv = np.linalg.inv(Amatrix)   ## 求出逆矩阵的

    # for i in range(h):
    #     for j in range(w):
    #         p = np.array([j, i, 1]).reshape((-1, 1))
    #         out = np.matmul(m2, p)
    #         out = np.matmul(A, out)
    #         out = np.matmul(m1, out)
    #         x = int(out[0][0])
    #         y = int(out[1][0])
    #         if x < 0 or x >= w or y < 0 or y >= h:
    #             continue
    #         rotateimg[y, x, :] = img[i, j, :]

    nh, nw = h, w
    for i in range(nh):
        for j in range(nw):
            out = np.array([j, i, 1]).reshape((-1, 1))
            p = np.matmul(Ainv, out)
            xo = p[0][0]
            yo = p[1][0]
            ixo = int(xo)
            iyo = int(yo)
            if xo < 0 or yo < 0 or xo >= w or yo >= h:
                rotateimg[i, j, :] = color
            elif (xo - ixo > 1e-10) or (yo - iyo > 1e-10):
                # scaleimg[i, j, :] = LINEARinsert(img, xo, yo, ixo, iyo, h, w)
                rotateimg[i, j, :] = NEARESTinsert(img, xo, yo, ixo, iyo, h, w)
            else:
                rotateimg[i, j, :] = img[iyo, ixo, :]

    cv2.imwrite(os.path.join(filepath, r'sunoray_rotate%s.jpg'%str(angle)), rotateimg)

if __name__ == "__main__":
    rotate_image()