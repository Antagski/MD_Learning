import numpy as np
import math

class Alloy():
    def __init__(self, box_size=np.array([50, 50, 50]), split_axis='z', num_split=np.array(2),
                 cell_loc=np.array([[0, 0.5], [0.5, 1]]), cell_size=np.array([0.2, 0.2])):
        self.box_size = box_size
        self.split_axis = split_axis
        self.num_split = num_split
        self.cell_loc = cell_loc
        self.cell_size = cell_size

        self.create_cell()

    def create_cell(self):
        cell_loc = np.zeros((1, 3))

        for i in range(self.num_split):
            size = math.ceil(1 / (self.cell_size[i]**3))
            loc = np.zeros((size, 3), dtype=int)
            if self.split_axis == 'x':
                idx = [0, 1, 2]
            elif self.split_axis == 'y':
                idx = [1, 2, 0]
            else:
                idx = [2, 0, 1]

            start_loc = math.ceil(self.cell_loc[i, 0] * self.box_size[idx[0]])
            stop_loc = math.floor(self.cell_loc[i, 1] * self.box_size[idx[0]])

            loc[:, [idx[0]]] = np.random.randint(start_loc, stop_loc, size=(loc.shape[0], 1), dtype=int)
            loc[:, [idx[1]]] = np.random.randint(1, self.box_size[idx[1]], size=(loc.shape[0], 1), dtype=int)
            loc[:, [idx[2]]] = np.random.randint(1, self.box_size[idx[2]], size=(loc.shape[0], 1), dtype=int)

            cell_loc = np.append(cell_loc, loc, axis=0)
        cell_loc = np.delete(cell_loc, 0, axis=0)
        cell_loc = cell_loc.astype(str)
        cell_loc = np.insert(cell_loc, 0, ['node'], axis=1)
        cell_loc = np.insert(cell_loc, 4, ['random'], axis=1)

        self.cell_loc_list = cell_loc

    def write_file(self):
        filename = "elementGrid.txt"
        with open(filename, 'w') as f:
            f.write(f"box {self.box_size[0]} {self.box_size[1]} {self.box_size[2]}\n")

        with open(filename, 'a') as f:
            np.savetxt(f, self.cell_loc_list, fmt='%s', delimiter=' ')


if __name__ == '__main__':
    box_size = np.array([100, 200, 800])
    split_axis = 'z'
    num_split = np.array(3)
    cell_loc = np.array([[0, 0.33], [0.33, 0.66], [0.66, 1]])
    cell_size = np.array([0.2, 0.5, 0.2])
    alloy = Alloy(box_size, split_axis, num_split, cell_loc, cell_size)
    alloy.write_file()
