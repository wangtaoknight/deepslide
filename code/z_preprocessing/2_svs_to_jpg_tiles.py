import argparse
import os
from math import ceil
from os import listdir
from os.path import isfile, join

import openslide
from PIL import Image

'''简单总结程序：
        将大的WSI图像保存为小的jpg图像，在10000*10000的水平上，在0级下进行除以三的滤镜缩放，然后进行保存。
'''

compression_factor = 3
window_size = 10000
Image.MAX_IMAGE_PIXELS = 1e10


def output_jpeg_tiles(image_name, output_path):  # converts svs image with meta data into just the jpeg image
    '''输入image_name是单张svs图像的绝对路径。 output_path是输出保存的文件'''

    img = openslide.OpenSlide(image_name)
    width, height = img.level_dimensions[0]

    increment_x = int(ceil(width / window_size))   #hang
    increment_y = int(ceil(height / window_size))  #lie

    print("converting", image_name, "with width", width, "and height", height)

    for incre_x in range(increment_x):  # have to read the image in patches since it doesn't let me do it for larger things
        for incre_y in range(increment_y):

            begin_x = window_size * incre_x
            end_x = min(width, begin_x + window_size)
            begin_y = window_size * incre_y
            end_y = min(height, begin_y + window_size)
            patch_width = end_x - begin_x
            patch_height = end_y - begin_y

            patch = img.read_region((begin_x, begin_y), 0, (patch_width, patch_height))
            patch.load()
            patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
            patch_rgb.paste(patch, mask=patch.split()[3])

            # compress the image
            patch_rgb = patch_rgb.resize((int(patch_rgb.size[0] / compression_factor), int(patch_rgb.size[1] / compression_factor)), Image.ANTIALIAS)

            # save the image
            output_subfolder = join(output_path, image_name.split('/')[-1][:-4])
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)
            output_image_name = join(output_subfolder, image_name.split('/')[-1][:-4] + '_' + str(incre_x) + '_' + str(incre_y) + '.jpg')
            patch_rgb.save(output_image_name)

# 创建了一个参数解析器
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, default=r'F:\camelyon_tumor\train\tumor', help="input folder")
parser.add_argument("--output_folder", type=str,default=r'F:\camelyon_tumor\train\normal', help="output folder")
parser.add_argument("--start_at", type=str, default=None, help="resume from a certain filename") #从某个具体的文件恢复，继续转换
args = parser.parse_args()

input_folder = args.input_folder
output_folder = args.output_folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_names = [f for f in listdir(input_folder) if isfile(join(input_folder, f))]
if '.DS_Store' in image_names:
    image_names.remove('.DS_Store') # .DS_Store是mac os中默认生成的一个隐藏文件，保存文件的属性信息

if args.start_at is not None:
    start = image_names.index(args.start_at)    #索引文件名对应的index 0，1，2...
    print("skipping the first", start)          # 对应的索引为start，从此处开始
    image_names = image_names[start + 2:]

for image_name in image_names:
    full_image_path = input_folder + '/' + image_name    #此处连接父目录与文件名用的是字符串假发，也可以用os.join()
    output_path = output_folder + '/'
    output_jpeg_tiles(full_image_path, output_path)  # 处理单张的svs文件，将其转换为jpeg进行保存
