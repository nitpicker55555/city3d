import trimesh
import os
import time
def load_and_merge_obj_files(folder_path):
    """
    Load all OBJ files in a specified folder and merge them into a single mesh.

    Parameters:
    folder_path (str): The path to the folder containing OBJ files.

    Returns:
    trimesh.Trimesh: A merged mesh object containing all OBJ files from the folder.
    """
    # 确保传入的路径存在
    if not os.path.exists(folder_path):
        print("The provided folder path does not exist.")
        return None

    # 初始化一个列表来存储加载的网格
    meshes = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.obj'):  # 确认文件扩展名是.obj
            file_path = os.path.join(folder_path, filename)
            try:
                # 加载网格并添加到列表中
                mesh = trimesh.load(file_path, force='mesh')
                meshes.append(mesh)
                print(f"Loaded mesh: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

    # 如果加载了任何网格，将它们合并
    if meshes:
        # 合并所有网格
        merged_mesh = trimesh.util.concatenate(meshes)
        print("All meshes have been merged.")
        return merged_mesh
    else:
        print("No meshes were loaded.")
        return None
start_time=time.time()
# 使用示例
folder_path = r'C:\Users\TUM_LfK\Documents\Python Scripts\submesh'  # 将此路径替换为你的文件夹路径
merged_mesh = load_and_merge_obj_files(folder_path)

# 如果你需要保存合并后的网格，可以这样做：
# if merged_mesh:
#     merged_mesh.export('merged_mesh.obj')
#     print("Merged mesh has been saved.")
print(time.time()-start_time)