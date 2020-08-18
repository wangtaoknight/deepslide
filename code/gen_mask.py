import get_ground
import numpy as np
import math
from PIL import Image
import cv2
"""
Annotation：
    本程序主要用以从.xml中生成二值mask图像
    dilate_bin_image是在线性化后进行膨胀操作，一个是自己写的，一个是网上的代码
    liner——image是将xml中读取的离散点连成一个封闭的线框，1-2-3—...-n-1
    tian-chong是将线性化之后的线框图像填补成完整的mask图像
Metho：
    用的时候调用gen_mask(path),返回值为二值化的mask
"""

#自己写的膨胀代码，只是简单的扩大标注点的范围，不适应其他领域的膨胀操作
def dilate_bin_image(bin_image, kernel):
    muban = bin_image.copy()
    y = int((kernel.shape[0]-1)/2)
    x = int((kernel.shape[1]-1)/2)
    for i in range(bin_image.shape[0]):
        if i<y:
            continue
        for j in range(bin_image.shape[1]):
            if j<x:
                continue
            try:
                fugai = muban[i-y:i+y+1,j-x:j+x+1]
                if fugai.sum()>0:
                    bin_image[i,j] = 1
            except:
                continue
    return bin_image

#此程序为网上，进行膨胀操作。效果和自己写的功能上差别不大
def dilate_bin_imagekk(bin_image, kernel):
    """
    dilate bin image
    Args:
        bin_image: image with 0,1 pixel value
    Returns:
        dilate image
    """
    kernel_size = kernel.shape[0]
    bin_image = np.array(bin_image)
    if (kernel_size%2 == 0) or kernel_size<1:
        raise ValueError("kernel size must be odd and bigger than 1")
    if (bin_image.max() != 1) or (bin_image.min() != 0):
        raise ValueError("input image's pixel value must be 0 or 1")
    d_image = np.zeros(shape=bin_image.shape)
    center_move = int((kernel_size-1)/2)
    for i in range(center_move, bin_image.shape[0]-kernel_size+1):
        for j in range(center_move, bin_image.shape[1]-kernel_size+1):
            d_image[i, j] = np.max(bin_image[i-center_move:i+center_move,j-center_move:j+center_move])
    return d_image

#根据标注的点连通标注区域，生成mask
def liner_image(lin_image,x_input,y_input ):
    def liner(image,x1,y1,x2,y2):
        if (x1!=x2) or (y1!=y2):
            x_bu =round((x1-x2)/(abs(x1-x2)+0.1))
            y_bu = round((y1 - y2) / (abs(y1 - y2) + 0.1))
            x1 = x1-x_bu
            x1 = int(x1)
            image[y1,x1] = 1
            y1 = y1 - y_bu
            y1 = int(y1)
            image[y1,x1] = 1
            image = liner(image=image,x1=x1,y1=y1,x2=x2,y2=y2)
        return image

    inde = 0
    x_s = x_input[0]
    y_s = y_input[0]
    num_i = len(x_input)
    for i in range(num_i):
        if i==num_i-1:
            lin_image = liner(image=lin_image, x1=x_input[inde], y1=y_input[inde], x2=x_s, y2=y_s)
            continue
        x = x_input[inde]
        y = y_input[inde]
        x_input.pop(inde)
        y_input.pop(inde)
        ou_x = (np.array(x_input)-x)**2
        ou_y = (np.array(y_input)-y)**2
        ou =ou_x +ou_y
        inde = np.argmin(ou)
        lin_image = liner(image=lin_image,x1=x,y1=y,x2=x_input[inde],y2=y_input[inde])
    return lin_image

def tian_chong(mask):
    '''

    Args:
        mask:0—1image
    Returns:
    '''
    # path_mask = r'F:\camelyon_tumor\tumor\mask_855new.jpg'
    # mask = cv2.imread(path_mask)
    mask = cv2.merge((mask,mask,mask))
    mask = np.uint8(mask)
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
    return img_cun

# 其他程序为调用子程序。本程序中生成mask以及ROI的目标区域
def gen_mask(input_path):
    xml_path = input_path
    zhi = get_ground.get_ground(xml_path)
    init = 0
    sum_img = list()
    for num_roi in zhi[0]:
        lie = np.array(zhi[1][init:init+num_roi])
        row = np.array(zhi[2][init:init+num_roi])
        lie = lie - lie.min()
        row = row - row.min()
        mask = np.zeros([row.max()+1,lie.max()+1])
        for i in range(num_roi):
            mask[row[i],lie[i]] = 1
        mask = liner_image(lin_image=mask,x_input=list(lie),y_input=list(row))      # 将图像中断点连上
        mask_cun = dilate_bin_image(bin_image=mask,kernel=np.ones([7,3]))
        mask_cun = mask_cun*255
        mask_tian = tian_chong(mask_cun)
        # mask_cun = Image.fromarray(np.uint8(mask_cun))
        # mask_tian = Image.fromarray(np.uint8(mask_tian))   #tu
        # mask_cun.save(r'F:\camelyon_tumor\tumor\mask_%dnew.jpg'%init)    调用的时候不用再进行保存
        # mask_tian.save(r'F:\camelyon_tumor\tumor\mask_tian_%dnew.jpg'%init)
        init = init +num_roi
        sum_img.append(mask_tian)
    return  sum_img





if __name__ =='__main__' :
    xml_path = r'F:\camelyon_tumor\tumor\tumor_001.xml'
    sum_img = gen_mask(xml_path)
    for img in sum_img:
        img = Image.fromarray(np.uint8(img))
    img.show()





