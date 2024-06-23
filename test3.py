import json
from datetime import datetime, timedelta
import trimesh
import concurrent.futures
import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
from pyproj import Transformer
# from read_height import get_height_by_lon_lat
from pyproj import CRS, Transformer

from tqdm import tqdm
from pyproj import Proj, transform
from get_sun_direction import calculate_sunray_direction_vector
df = pd.read_csv(r"C:\Users\Morning\Downloads\munich_trans_facade_samples\munich_trans_facade_samples.csv")
print(len(df))