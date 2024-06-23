import trimesh
import numpy as np
import time

# Start timer for loading mesh
start_time = time.time()
mesh = trimesh.load('C:\\Users\\TUM_LfK\\Documents\\Python Scripts\\combined_mesh.obj')
print(f"Time taken to load mesh: {time.time() - start_time} seconds")

# Determine bounds and divisions
longitude_bounds = (np.min(mesh.vertices[:, 0]), np.max(mesh.vertices[:, 0]))
latitude_bounds = (np.min(mesh.vertices[:, 1]), np.max(mesh.vertices[:, 1]))
latitude_divisions = 10
longitude_divisions = 11

# Calculate step sizes for latitude and longitude
lat_step = (latitude_bounds[1] - latitude_bounds[0]) / latitude_divisions
lon_step = (longitude_bounds[1] - longitude_bounds[0]) / longitude_divisions

# Prepare a grid for storing vertex groups
vertex_groups = [[[] for _ in range(longitude_divisions)] for _ in range(latitude_divisions)]

# Assign vertices to appropriate groups based on their coordinates
for i, vertex in enumerate(mesh.vertices):
    lat_idx = int((vertex[1] - latitude_bounds[0]) / lat_step)
    lon_idx = int((vertex[0] - longitude_bounds[0]) / lon_step)
    lat_idx = min(lat_idx, latitude_divisions - 1)
    lon_idx = min(lon_idx, longitude_divisions - 1)
    vertex_groups[lat_idx][lon_idx].append(i)

# Initialize a grid for sub-meshes
mesh_grid = [[None for _ in range(longitude_divisions)] for _ in range(latitude_divisions)]

# Create sub-meshes and export each as a separate .obj file
for lat_idx in range(latitude_divisions):
    for lon_idx in range(longitude_divisions):
        indices = vertex_groups[lat_idx][lon_idx]
        if indices:
            submesh = mesh.submesh([indices], append=True)
            mesh_grid[lat_idx][lon_idx] = submesh
            # Exporting sub-mesh
            filename = f'submesh_{lat_idx}_{lon_idx}.obj'
            submesh.export(f'C:\\Users\\TUM_LfK\\Documents\\Python Scripts\\{filename}')
