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

        # 计算临界距离
        self.critical_distance = self.box_size[0] * self.cell_size[0]

        self.create_cell()

    def distance_check(self, loc, existing_locs):
        """ 检查 loc 是否与 existing_locs 中的任何一个点过近 """
        if existing_locs.size == 0:
            return False
        distances = np.linalg.norm(existing_locs - loc, axis=1)
        return np.any(distances < self.critical_distance)

    def create_cell(self):
        cell_loc = np.zeros((1, 3))
        existing_locs = np.empty((0, 3))

        for i in range(self.num_split):
            size = math.floor(1 / (self.cell_size[i] ** 3))
            loc = np.zeros((size, 3), dtype=int)
            if self.split_axis == 'x':
                idx = [0, 1, 2]
            elif self.split_axis == 'y':
                idx = [1, 2, 0]
            else:
                idx = [2, 0, 1]

            start_loc = math.ceil(self.cell_loc[i, 0] * self.box_size[idx[0]])
            stop_loc = math.floor(self.cell_loc[i, 1] * self.box_size[idx[0]])

            for j in range(size):
                while True:
                    new_loc = np.zeros(3, dtype=int)
                    new_loc[idx[0]] = np.random.randint(start_loc, stop_loc)
                    new_loc[idx[1]] = np.random.randint(0, self.box_size[idx[1]])
                    new_loc[idx[2]] = np.random.randint(0, self.box_size[idx[2]])

                    if not self.distance_check(new_loc, existing_locs):
                        loc[j] = new_loc
                        existing_locs = np.append(existing_locs, [new_loc], axis=0)
                        print(j)
                        break

            cell_loc = np.append(cell_loc, loc, axis=0)
        cell_loc = np.delete(cell_loc, 0, axis=0)

        # 确保行的唯一性
        cell_loc = np.unique(cell_loc, axis=0)
        np.random.shuffle(cell_loc)

        cell_loc = cell_loc.astype(str)
        cell_loc = np.insert(cell_loc, 0, ['node'], axis=1)
        cell_loc = np.insert(cell_loc, 4, ['random'], axis=1)

        self.cell_loc_list = cell_loc

    def write_file(self, filename="elementGrid.txt"):
        # filename = "elementGrid.txt"
        with open(filename, 'w') as f:
            f.write(f"box {self.box_size[0]} {self.box_size[1]} {self.box_size[2]}\n")

        with open(filename, 'a') as f:
            np.savetxt(f, self.cell_loc_list, fmt='%s', delimiter=' ')


if __name__ == '__main__':
    """
    box_size = np.array([100, 200, 800])
    split_axis = 'z'
    num_split = np.array(3)
    cell_loc = np.array([[0, 0.33], [0.33, 0.66], [0.66, 1]])
    cell_size = np.array([0.2, 0.5, 0.2])
    alloy = Alloy(box_size, split_axis, num_split, cell_loc, cell_size)
    alloy.write_file()
    """

    from Alloy_Database import grand_bar, cubic_13nm, cubic_12nm, cubic_5nm, cubic_7nm, cubic_9nm, cubic_11nm

    alloy_configurations = {

        'cubic_5nm': cubic_5nm,
    }

    for name, alloy in alloy_configurations.items():
        _alloy = Alloy(alloy["box_size"], alloy["split_axis"], alloy["num_split"],
                       alloy["cell_loc"], alloy["cell_size"])
        _alloy.write_file(filename=f"{name}.txt")
