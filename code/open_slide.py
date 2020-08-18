import openslide
import cv2 as cv
import numpy as np
from PIL import Image
import time
import math
import get_ground
import gen_mask


def sao_miao(img_roi,mask):
    '''
    定义处理的窗口为512*512，定义处理阈值为默认70%，将非保留区域重新赋值为零
    Args:
        img_roi:
        mask: 0-1 mask of ROI
    Returns: img_roi
    '''
    thresh = 0.7
    s_c = 1024
    n_i = math.ceil(img_roi.shape[0]/s_c)
    n_j = math.ceil(img_roi.shape[1]/s_c)
    for i in range(n_i-1):
        for j in range(n_j):
            try:
                mask_patch = mask[(i+1)*s_c-s_c:(i+1)*s_c,(j+1)*s_c-s_c:(j+1)*s_c]
                if mask_patch.sum()/math.pow(s_c,2) < thresh:
                    img_roi[(i+1)*s_c - s_c:(i+1)*s_c,(j+1)*s_c-s_c:(j+1)*s_c,:] = 255
            except:
                mask_patch = mask[(i+1)*s_c - s_c:(i + 1) * s_c, (j + 1) * s_c - s_c:]
                if mask_patch.sum()/(mask_patch.shape[0]*mask_patch.shape[1])<thresh:
                    img_roi[(i + 1) * s_c - s_c:(i + 1) * s_c, (j + 1) * s_c - s_c:(j + 1) * s_c,:] = 255
    return img_roi



if __name__=='__main__':

    slide_path = r'F:\camelyon_tumor\tumor\tumor_001.tif'
    xml_path = r'F:\camelyon_tumor\tumor\tumor_001.xml'

    slide = openslide.OpenSlide(slide_path)
    print(slide.level_dimensions)
    a = slide.level_dimensions[8]
    print('a',a)
    print('slide_count',slide.level_count)


    zhi = get_ground.get_ground(xml_path)
    mask_img = gen_mask.gen_mask(xml_path)
    st = 0      # 第n张图像的起始位置的对应序列
    n = 0       #处理第n张图片
    for i in zhi[0]:
        s = np.array(zhi[1][st: st+i])
        y = np.array(zhi[2][st: st+i])
        s_z = s.min()
        s_y = s.max()
        h_x = y.max()
        h_s = y.min()

        kk = slide.read_region((s.min(), y.min()),0,(s.max()-s.min(), y.max()-y.min())) #slide.level_dimensions[4]
        kk = kk.convert('RGB')
        img_roi = np.array(kk)
        mask = mask_img[n]
        img_roi = sao_miao(img_roi=img_roi,mask=mask)
        kk = Image.fromarray(np.uint8(img_roi))
        print('----------读取区域完成----------')
        # print(type(kk))
        # kk = Image.fromarray(kk)
        # kk.show()
        # kk.show()

        tu_name = slide_path.split('\\')[-1]
        tu_name = tu_name.split('.')[0]
        print('将其转换为了RGB图像')
        kk.save(r'F:\camelyon_tumor\tumor\\' + tu_name+ '_%d.jpg'%n)
        print('----------保存图像完毕----------')
        st = st+i
        n = n+1


