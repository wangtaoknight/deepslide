import glob
import os
import numpy as np
import xml.etree.ElementTree as ET
import argparse
'''
    顾名思义，是得到边界
    本程序主要根据cameloyn16图像中的.xml注释来生成其点集。将结果保存在变量zhi中返回
    zhi[0]中保存的是每个标记区域中包含的点集数，几个区域就对应几个几个值
    zhi[1]保存X的值  zhi[2]保存Y的值
    使用的时候调用get_ground(path)，给出path即可
'''

def get_ground(input_path):
    tree = ET.parse(input_path)
    root = tree.getroot()
    menu = root[0]
    Roi_num = len(menu)
    biao = list()
    X = list()
    Y = list()
    for i in range(Roi_num):
        biao.append(len(menu[i][0]))
        for j in range(len(menu[i][0])):
            X.append(round(float(menu[i][0][j].attrib['X'])))
            Y.append(round(float(menu[i][0][j].attrib['Y'])))
    zhi = [biao,X,Y]
    return  zhi









if __name__ == '__main__':
    path = r'F:\camelyon_tumor\tumor\tumor_001.xml'
    zhi = get_ground(path)
    print(type(zhi))
    print(zhi)