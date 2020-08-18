import time

import cv2
import os
import numpy as np
from PIL import Image
import open_slide
import cv2
import matplotlib.pyplot as plt
import openslide
import math
'''
    本程序仅仅用来测试code,再写code的过程中使用
'''

def ceshi_1():
    path_mask = r'F:\camelyon_tumor\tumor\mask_855new.jpg'
    mask = cv2.imread(path_mask)

    bin_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(bin_mask, 0, 255, cv2.THRESH_BINARY)
    # bin_mask = cv.imread(path_mask)

    # 寻找轮廓
    # 也可以这么写：
    # binary,contours, hierarchy = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # 这样，可以直接用contours表示
    h,c = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(mask,h,-1,(255, 255, 255),-1,lineType=cv2.LINE_AA)
    img_cun = img[:,:,0]
    plt.imshow(img_cun,cmap='gray')
    plt.show()

def ceshi_2():
    path_img = r'F:\camelyon_tumor\tumor\cc.jpg'
    path_mask = r'F:\camelyon_tumor\tumor\cc_mask.jpg'
    img_roi = Image.open(path_img)
    mask = Image.open(path_mask)
    img_roi = np.array(img_roi)
    mask = np.array(mask)
    img_roi=open_slide.sao_miao(img_roi=img_roi,mask=mask)
    img_roi = Image.fromarray(np.uint8(img_roi))
    img_roi.show()

def jian_zhuan():
    '''
    本程序计划将一整个的wsi进行分割，保存成小的三通道之后再重新组合起来。主要是考虑内存的原因。放不下
    Returns:

    '''
    slide_path = r'F:\camelyon_tumor\tumor\tumor_001.tif'
    slide = openslide.OpenSlide(slide_path)
    print(slide.level_dimensions)
    size_slide = slide.level_dimensions[0]
    num_l = math.floor(size_slide[0]/6)
    num_h = math.floor(size_slide[1]/12)
    li1 = list()
    li2 = list()
    li3 = list()
    for i in range(9):
        for j in range(3):
            k = slide.read_region((i*num_l,j*num_h),0,(num_l,num_h))
            k = k.convert('RGB')
            k = np.array(k)
            k = np.uint8(k)
            li1.append(k)
            del k
        break
    del slide
    img = np.array(li1[0])
    li1.pop(0)
    img = np.hstack((img,li1[0]))
    li1.pop()
    img = np.hstack((img, li1[0]))
    img = np.hstack((img,li1[2]))
    del li1
    img = Image.fromarray(np.uint8(img))
    img.save(r'F:\camelyon_tumor\tumor\row_lie.jpg')
    # img.show()

    # kk = slide.read_region((0,0),0,(1000,2000))
    # kk = kk.convert('RGB')
    # kk.show()
    # return kk

def for_files()->int:
    '''
    本程序主要用以测试循环遍历程序，找到文件夹中指定的文件
    Returns:

    '''
    i = 0
    for parent,dirname,filenames in os.walk('G:/panda/train_images'):
        print(filenames)
        time.sleep(10)
        for filename in filenames:
            print(os.path.join(parent,filename))
            print(type(filename))
            if i>=10:
                break
            i +=1
        break
    # 继续读取wsi.tif然后保存jpg



if __name__=='__main__':
    # a = np.ones([3,4,2])
    # b = np.zeros([3,2,2])
    # c = np.hstack((a,b))
    # for_files()

    i = 0
    for parent,dirname,filenames in os.walk('G:/panda/train_images'):
        print(filenames)
        # time.sleep(10)
        for filename in filenames:
            print(os.path.join(parent,filename))
            print(type(filename))
            if i>=10:
                break
            i +=1
        print('测试内循环之后的输出')