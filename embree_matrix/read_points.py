import numpy as np
import os

# 设置你的文件夹路径
folder_path = r'D:\puzhen\hi_structure\city3d\loacations_closed'

# 遍历文件夹中的所有文件
for file in os.listdir(folder_path):
    if file.endswith('.npy'):
        # 构造文件的完整路径
        file_path = os.path.join(folder_path, file)

        # 加载npy文件
        array = np.load(file_path)

        # 计算数组中0的个数
        zero_count = np.sum(array == 1)

        # 打印结果
        print(f'File {file} has {zero_count} zeros.')
