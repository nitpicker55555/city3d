import numpy as np

aa=np.load('intensity.npy')
import numpy as np

# 假设 matrix 是你的原始矩阵
# 例如：
matrix =aa
# 指定要插入0的列的索引位置
indices_to_insert = [442724, 442725, 442726, 442727, 816380, 1102633, 1102634, 1102635, 1124880, 1124985, 1124986, 1124987, 1124988, 1124989, 1124990, 1124991, 1124992, 1124993, 1302683, 1376613, 1376614, 1376615]

# 计算插入后的新矩阵的总列数
new_col_count = matrix.shape[1] + len(indices_to_insert)

# 创建一个新的矩阵，初始化为0（因为要插入的是0列）
new_matrix = np.zeros((matrix.shape[0], new_col_count))

# 计算每个插入点之前应保留的原始列数
insert_positions = np.zeros(new_col_count, dtype=bool)
insert_positions[indices_to_insert] = True

# 计算原始数据应该复制到新矩阵的位置
target_indices = np.arange(new_col_count)[~insert_positions]

# 将原始矩阵数据复制到新矩阵的正确位置
new_matrix[:, target_indices] = matrix
print(new_matrix.shape)
np.save("light_intensity.npy", new_matrix)
# new_matrix 现在包含了插入的0列
