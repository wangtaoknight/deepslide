import os
import shutil
import time
import glob
import cv2
from matplotlib import pyplot as plt
from PIL import Image
# 因为patch的数量太大，动辄上万张，在用UI界面进行剪切复制的时候很容易卡顿，所以写程序进行批处理
# 本程序可以运行移动指定类型文件到指定目录下

def move_jpg():
    # 本程序使用os.walk，可以将本文件夹、子文件夹下所有的jpg进行移动
    sc_path = '/home/public2/Lan/data_camelyon16/all_npy/all_patch/train_patch/tumor'
    aim_path = '/home/public2/Lan/data_camelyon16/all_npy/all_patch/valid_patch/tumor'
    i = 1
    for folderName, subfolders, filenames in os.walk(sc_path):
        print(folderName)
        for filename in filenames:
            if i>18260:
                break
            if '.jpg' in filename:
                print(filename)
                try:
                    shutil.move(folderName+'/'+filename,aim_path+'/'+filename)
                    i = i+1
                except OSError:
                    print('出错！')

def move_mask():
    # 本程序使用os.walk，可以将本文件夹、子文件夹下所有的jpg进行移动
    sc_path = 'G:/mars/tumor_mask/'
    aim_path = 'G:/mars/data/tumor/'
    i = 1
    for folderName, subfolders, filenames in os.walk(sc_path):
        print(folderName)
        for filename in filenames:
            if '_' not in filename:
                print(filename)
                try:
                    shutil.move(folderName+filename, aim_path+filename)
                except OSError:
                    print('出错！')

def copy_file(sr_path,aim_path):
    # 此函数定义为将sr_path下的文件复制到aim_path文件夹下
    # i=1
    for folderName, subfolders, filenames in os.walk(sr_path):
        print(folderName)
        for filename in filenames:
            # if i>14608:
            #     break
            if '.tif' in filename:
                print(filename)
                try:
                    shutil.copy2(folderName+'/'+filename,aim_path +'/'+filename)
                    # i +=1
                except OSError:
                    print('出错！')

def show_jpeg():
    def xianshi(pics):
        plt.subplot(1, 3, 1)
        plt.imshow(pics[0])
        # plt.title('patch_normal')
        plt.xticks([])
        plt.yticks([])
        plt.subplot(1, 3, 2)
        plt.imshow(pics[1])
        plt.title('patch_tumor')
        plt.xticks([])
        plt.yticks([])
        plt.subplot(1, 3, 3)
        plt.imshow(pics[2])
        # plt.title('patch_normal')
        plt.xticks([])
        plt.yticks([])
        plt.savefig('/home/public2/Lan/data_camelyon16/all_npy/all_patch/result_train/imags/tumor.jpg')
        plt.show()
    sr_path = '/home/public2/Lan/data_camelyon16/all_npy/all_patch/valid_patch/tumor/'
    paths =glob.glob(sr_path+'*.jpg')
    i=1
    normal = list()
    for path in paths:
        if i<31:
            i +=1
            continue
        elif i>34:
            break
        # img = cv2.imread(path, 0)
        img = Image.open(path)
        normal.append(img)
        i +=1
    xianshi(normal)


if __name__ =='__main__':
    move_mask()