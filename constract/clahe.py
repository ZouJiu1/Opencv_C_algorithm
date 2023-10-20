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
    # pth = os.path.join(filepath, r'..\Photo2.jpg')
    img = cv2.imread(pth, 0)
    height, width = img.shape
    # img = cv2.resize(img, (width//4, height//4))
    height, width = img.shape
    tile_h = 2 * 2 * 2
    tile_w = 2 * 2 * 2
    thresh = 20 * 2
    pad_h = int(np.ceil(height / tile_h) * tile_h - height)
    pad_w = int(np.ceil(width / tile_w) * tile_w - width)
    padimg = np.pad(img, ((pad_h // 2, pad_h - pad_h//2), (pad_w // 2, pad_w - pad_w // 2)), \
                                mode='constant', constant_values=(0, 0))
    height, width = padimg.shape
    block_h = height // tile_h
    block_w = width // tile_w
    clipthresh = 60+200 ##thresh * block_h * block_w / 256

    # clahe = cv2.createCLAHE(2, (20, 20))
    # image = clahe.apply(img)
    # cv2.imshow('img', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    nimage = np.zeros_like(padimg)
    for ih in range(0, tile_h):
        for jw in range(0, tile_w):
            image = img[ih * block_h:(ih + 1) * block_h, jw * block_w:(jw + 1) * block_w]
            h, w = image.shape
            count = np.zeros(256)
            for i in range(h):
                for j in range(w):
                    count[image[i, j]] += 1
            largezero = []
            for i in range(256):
                if count[i] > 0:
                    largezero.append(i)
            largethresh = 2
            need = set()
            while largethresh > 0:
                if largethresh < 1e-2:
                    break
                largethresh = 0
                now = []
                for i in range(256):
                    if count[i] > clipthresh:
                        largethresh += count[i] - clipthresh
                        count[i] = count[i] - clipthresh
                        if i in need:
                            need.remove(i)
                    elif count[i] - clipthresh == 1e-6:
                        continue
                    else:
                        need.add(i)
                if largethresh > 0:
                    for i in need:
                        count[i] += largethresh / len(need)

            cumsum = np.cumsum(count)
            nimg = np.zeros_like(image)
            areas = h * w
            finalnum = np.zeros_like(cumsum)
            for i in range(256):
                finalnum[i] = (256 / areas) * cumsum[i] - 1
            kk = list(cumsum)
            kkk = list(finalnum)
            for i in range(h):
                for j in range(w):
                    
                    nimg[i, j] = (256 / areas) * cumsum[image[i, j]] - 1
                    # nimg[i, j] = (len(largezero) / areas) * cumsum[image[i, j]] - 1
            nimg[nimg < 0] = 0
            nimg[nimg > 255] = 255
            
            nimage[ih * block_h : ih * block_h + image.shape[0], jw * block_w : jw * block_w + image.shape[1]] = nimg
            # countafter = np.zeros(256)
            # for i in range(h):
            #     for j in range(w):
            #         countafter[nimg[i, j]] += 1
            # plt.plot(range(len(countafter)), countafter)
            # plt.plot(range(len(countafter)), np.cumsum(countafter))
            # plt.show()
            # plt.close()
    img = np.concatenate([padimg, nimage], axis = 1)
    cv2.imwrite(os.path.join(filepath, r'clahe.jpg'), img)

if __name__ == "__main__":
    equal_histgray_image()