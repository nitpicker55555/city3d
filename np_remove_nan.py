import numpy as np

def remove_nan_rows(arr):
    """
    Remove rows containing NaN from a numpy array and record their indices.

    Parameters:
    arr (np.array): The input numpy array.

    Returns:
    tuple: A tuple containing:
        - np.array: The array with NaN containing rows removed.
        - list: The indices of the rows that were removed.
    """
    # 检查每一行是否包含NaN
    mask = np.any(np.isnan(arr), axis=1)
    # 找到不包含NaN的行
    filtered_arr = arr[~mask]
    # 获取包含NaN的行的索引
    removed_indices = np.where(mask)[0]
    np.save("points_removed_nan2.npy",filtered_arr)
    return filtered_arr, list(removed_indices)

# 示例使用
data = np.load('epsg25832_points.npy')
filtered_data, removed_indices = remove_nan_rows(data)

print("Filtered Data:")

# print(filtered_data)
print("Removed Indices:")
print((removed_indices))

print(len(removed_indices))
