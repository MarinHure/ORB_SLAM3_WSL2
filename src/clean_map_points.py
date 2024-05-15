import numpy as np
from scipy.spatial import cKDTree

def load_point_cloud(file_path):
    """
    Load point cloud data from a PLY file.

    Args:
    - file_path (str): Path to the PLY file.

    Returns:
    - numpy.ndarray: Array containing the point cloud data.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    data_start_index = lines.index('end_header\n') + 1
    point_cloud_data = np.loadtxt(lines[data_start_index:])

    return point_cloud_data

def filter_point_cloud(point_cloud, min_neighbors, point_distance):
    """
    Filter out points from the point cloud that are too far away and do not have enough neighbors.
    
    Args:
    - point_cloud (numpy.ndarray): Array containing the point cloud data.
    - max_distance (float): Maximum distance threshold for filtering points.
    - min_neighbors (int): Minimum number of neighbors required for a point to be retained.
    
    Returns:
    - numpy.ndarray: Filtered point cloud data.
    """
    
    tree = cKDTree(point_cloud[:, :3])
    neighbors = tree.query_ball_point(point_cloud[:, :3], r=point_distance)
    num_neighbors = np.array([len(n) for n in neighbors])
    print("Number of neighbors:", num_neighbors)
    filtered_indices = (point_cloud[:, :3] != 0).any(axis=1) & (num_neighbors >= min_neighbors)
    print("Filtered indices:", filtered_indices)
    filtered_point_cloud = point_cloud[filtered_indices]
    print("Filtered point cloud:", filtered_point_cloud)
    
    return filtered_point_cloud

def save_point_cloud(point_cloud, file_path):
    """
    Save filtered point cloud data to a PLY file.

    Args:
    - point_cloud (numpy.ndarray): Filtered point cloud data.
    - file_path (str): Path to save the filtered PLY file.
    """
    with open(file_path, 'w') as f:
        f.write('ply\n')
        f.write('format ascii 1.0\n')
        f.write('element vertex {}\n'.format(len(point_cloud)))
        f.write('property float x\n')
        f.write('property float y\n')
        f.write('property float z\n')
        f.write('end_header\n')

        for point in point_cloud:
            f.write('{} {} {}\n'.format(point[0], point[1], point[2]))


# File paths
input_file_path = 'Map_Points.ply'
output_file_path = 'Map_Points_Cleaned.ply'

# Load point cloud data
point_cloud = load_point_cloud(input_file_path)

if point_cloud is None:
    print("Error: Unable to load point cloud data from file.")
    exit(1)
    
# Filter point cloud data
point_distance = 0.07
min_neighbors = 8   # Minimum number of neighbors required
filtered_point_cloud = filter_point_cloud(point_cloud, min_neighbors, point_distance)

# Check if filtered_point_cloud is empty (indicating all points were filtered out)
if len(filtered_point_cloud) == 0:
    print("Error: No points remain after filtering.")
    exit(1)

# Save filtered point cloud data
save_point_cloud(filtered_point_cloud, output_file_path)
