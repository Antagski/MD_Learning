import numpy
import ovito.data
import numpy as np
import ovito.io
import matplotlib.pyplot as plt
import PySide6.QtWidgets
from ovito.modifiers import CommonNeighborAnalysisModifier, SliceModifier


def read_file() -> ovito.pipeline.Pipeline:
    PATH = 'D:/Atomsk/Model/合金拉伸/CoNiCr/拉伸/Outputs/30_60_240/CoCrNiTension.xyz'
    pipeline = ovito.io.import_file(PATH)
    print("Finish read_file")
    return pipeline


def compute(pipeline: ovito.pipeline.Pipeline) -> None:
    common = CommonNeighborAnalysisModifier()
    pipeline.modifiers.append(common)
    num_frames = pipeline.source.num_frames
    rate = np.zeros((num_frames - 1, 5))
    # print(f"{num_frames}")
    for idx in range(num_frames - 1):
        data = pipeline.compute(idx)
        structure_types = data.particles['Structure Type']
        _rate = _get_rate(structure_types)
        rate[idx, :] = _rate
    rate = rate / np.sum(rate, axis=1, where=[0])
    print("Finish compute")
    np.savetxt("rate.txt", rate, fmt='%d')


def _get_rate(structure_types: ovito.data.ParticleType) -> numpy.array:
    data = np.array(structure_types)
    _rate = np.zeros((1, 5))
    for type in range(4):
        _rate[0, [type]] = np.sum(data == type)
    return _rate


def plot_rate() -> None:
    rate = np.loadtxt("rate.txt", converters=float)
    rate = rate / np.sum(rate[0, :])
    plt.figure()
    for idx in range(rate.shape[1]):
        plt.plot(range(rate.shape[0]), rate[:, idx])
    plt.legend([f"Type:{i}" for i in range(5)])
    plt.show(block=True)


def main():
    app = PySide6.QtWidgets.QApplication()
    pipeline = read_file()
    compute(pipeline)
    # plot_rate()


if __name__ == '__main__':
    main()
