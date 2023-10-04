import os
import sys
filepath = os.path.abspath(__file__)
nam = filepath.split(os.sep)[-1]
filepath = filepath.replace(nam, "")
sys.path.append(filepath)

import cv2
import numpy as np

def scale_up():
    pth = os.path.join(filepath, r'..\shift\sunoray.png')
    img = cv2.imread(pth)
    h, w, c = img.shape
    scale_ratio = 2
    
    color = [255, 0, 0]
    nh, nw = int(h * scale_ratio), int(w * scale_ratio)
    scaleimg = np.zeros((nh, nw, 2 + 1))
    scaleimg[:, :, :] = color
    x0, y0 = 0, 0
    
    m1 = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]])
    s = np.array([[scale_ratio, 0, 0], [0, scale_ratio, 0], [0, 0, 1]])
    m2 = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]])
    
    A = np.matmul(np.matmul(m1, s), m2)  ##  m1 @ s @ m2
    Ainv = np.linalg.inv(A)   ## 求出逆矩阵的
    
    ## no inserting
    # for i in range(h):
    #     for j in range(w):
    #         p = np.array([j, i, 1]).reshape((-1, 1))
    #         out = np.matmul(A, p)
    #         xc = int(out[0][0])
    #         yc = int(out[1][0])
            
    #         if (xc - int(xc)) > 1e-6 or (yc - int(yc)) > 1e-6 or int(xc) >= nw or int(yc) >= nh:
    #             continue
    #         scaleimg[int(yc), int(xc), :] = img[i, j, :]

    for i in range(nh):
        for j in range(nw):
            out = np.array([j, i, 1]).reshape((-1, 1))
            p = np.matmul(Ainv, out)
            xo = p[0][0]
            yo = p[1][0]
            ixo = int(xo)
            iyo = int(yo)
            if xo < 0 or yo < 0 or xo >= w or yo >= h:
                scaleimg[i, j, :] = color
            elif (xo - ixo > 1e-10) or (yo - iyo > 1e-10):
                scaleimg[i, j, :] = LINEARinsert(img, xo, yo, ixo, iyo, h, w)
                # scaleimg[i, j, :] = NEARESTinsert(img, xo, yo, ixo, iyo, h, w)
            else:
                scaleimg[i, j, :] = img[iyo, ixo, :]

    cv2.imwrite(os.path.join(filepath, r'sunoray_x0y0_up%s_LINEAR.jpg'%str(scale_ratio)), scaleimg)

def LINEARinsert(image, xo, yo, ixo, iyo, h, w):
    p1 = [ixo, iyo]
    p2 = [ixo + 1, iyo]
    p3 = [ixo, iyo + 1]
    p4 = [ixo + 1, iyo + 1]
    
    if ixo + 1 >= w and iyo + 1 >= h:
        return image[iyo, ixo, :]
    elif ixo + 1 >= w and iyo < h:
        alpha = yo - iyo
        value = alpha * image[iyo + 1, ixo, :] + (1 - alpha) * image[iyo, ixo, :]
    elif iyo + 1 >= h and ixo < w:
        alpha = xo - ixo
        value = alpha * image[iyo, ixo + 1, :] + (1 - alpha) * image[iyo, ixo, :]
    else:
        alpha = xo - ixo
        y_val0 = alpha * image[iyo, ixo + 1, :] + (1 - alpha) * image[iyo, ixo, :]
        y_val1 = alpha * image[iyo + 1, ixo + 1, :] + (1 - alpha) * image[iyo + 1, ixo, :]
        
        alpha = yo - iyo
        value = alpha * y_val1 + (1 - alpha) * y_val0

    return value

def NEARESTinsert(image, xo, yo, ixo, iyo, h, w):
    origin = np.array([xo, yo])
    p1 = np.array([ixo, iyo])
    p2 = np.array([ixo + 1, iyo])
    p3 = np.array([ixo, iyo + 1])
    p4 = np.array([ixo + 1, iyo + 1])

    if ixo + 1 >= w and iyo + 1 >= h:
        return image[iyo, ixo, :]
    elif ixo + 1 >= w and iyo < h:
        ret = [p1, p3]
    elif iyo + 1 >= h and ixo < w:
        ret = [p1, p2]
    else:
        ret = [p1, p2, p3, p4]

    result = []
    for p in ret:
        d = np.sum(np.square(p - origin))
        result.append(d)
    
    index = np.argmax(result)
    x, y = ret[index][0], ret[index][1]
    return image[y, x, :]

if __name__ == "__main__":
    scale_up()
