import os
from os import listdir
from os.path import isfile, join
import argparse

'''
    说明：本程序是将指定文件夹下面的文件重新命名
'''
def get_image_paths(folder):
    ''' 本程序是解析文件路径代码程序，将目标文件夹下的所有文件路径放入image_paths中，
    注意：是绝对路径.
    '''
    image_paths = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    if join(folder, '.DS_Store') in image_paths:
        image_paths.remove(join(folder, '.DS_Store'))
    return image_paths

'''本行代码为参数解析器，创建了一个-—文件夹输入参数——，'''
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, help="input folder")
args = parser.parse_args()

image_paths = get_image_paths(args.input_folder)
# 本行代码是将每一个文件的路径中空格去掉，将‘_’用'-'来代替
for image_path in image_paths:
    clean_path = image_path.replace(' ', '')
    # clean_path = image_path.replace('_', '-')
    print(clean_path)
    os.rename(image_path, clean_path)
print(image_paths)