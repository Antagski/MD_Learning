import numpy as np
# 10A = 1nm


grand_bar = {
    'box_size': np.array([300, 300, 800]),
    'split_axis': 'z',
    'num_split': np.array(3),
    'cell_loc': np.array([[0, 0.33], [0.33, 0.66], [0.66, 1]]),
    'cell_size': np.array([0.2, 0.5, 0.2])
}

cubic_1nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.02])
}

cubic_3nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.06])
}

cubic_5nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.1])
}

cubic_7nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.14])
}

cubic_9nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.18])
}

cubic_12nm = {
    'box_size': np.array([500, 500, 500]),
    'split_axis': 'z',
    'num_split': np.array(1),
    'cell_loc': np.array([[0, 1]]),
    'cell_size': np.array([0.24])
}