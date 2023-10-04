import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np
from neighbor_insert import LINEARinsert, NEARESTinsert

def get():
    inpoint = np.array([[0, 0], [200, 0], [0, 200]], dtype=np.float32)
    outpoint = np.array([[0, 0], [100, 0], [0, 100]], dtype=np.float32)
    matrix = cv2.getAffineTransform(inpoint, outpoint)
    return matrix

def matrixMultiply():
    t = np.array([[1, 0, 100], [0, 1, 200], [0, 0, 1]])
    s = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]])
    A = np.matmul(t, s)
    return A

def get_rotate2D():
    A = cv2.getRotationMatrix2D((100, 100), angle=60, scale=1.0)
    return A

def notchange():
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
    ang  = np.array([[np.cos(angle), np.sin(angle), 0], [-np.sin(angle), np.cos(angle), 0], [0, 0, 1]]) # 逆时针
    m2 = np.array([[1, 0, -cw], [0, 1, -ch], [0, 0, 1]])
    
    p = np.array([[0, 0, 1], [0, h-1, 1], [w-1, 0, 1], [w - 1, h - 1, 1]])
    col_h = []
    col_w = []
    for i in p:
        i = i.reshape((-1, 1))
        out = np.matmul(m2, i)
        out = np.matmul(ang, out)
        out = np.matmul(m1, out)
        col_w.append(out[0][0])
        col_h.append(out[1][0])
    ratio_x = (np.max(col_w) - np.min(col_w)) / w
    ratio_y = (np.max(col_h) - np.min(col_h)) / h
    ratio = 1 / max(ratio_x, ratio_y)

    # A = cv2.getRotationMatrix2D((cw, ch), angle=angle * 360 / 2 / np.pi, scale=ratio)
    # rotateimg = cv2.warpAffine(img, A, (w, h))

    s = np.array([[ratio, 0, 0], [0, ratio, 0], [0, 0, 1]])
    A = np.matmul(np.matmul(np.matmul(m1, ang), s), m2)
    Ainv = np.linalg.inv(A)   ## 求出逆矩阵的
    
    # for i in range(h):
    #     for j in range(w):
    #         p = np.array([j, i, 1]).reshape((-1, 1))
    #         out = np.matmul(A, p)
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
                rotateimg[i, j, :] = LINEARinsert(img, xo, yo, ixo, iyo, h, w)
                # rotateimg[i, j, :] = NEARESTinsert(img, xo, yo, ixo, iyo, h, w)
            else:
                rotateimg[i, j, :] = img[iyo, ixo, :]

    cv2.imwrite(os.path.join(filepath, r'sunoray_getaffine%s.jpg'%str(angle)), rotateimg)

if __name__=="__main__":
    get()
    matrixMultiply()
    get_rotate2D()
    notchange()