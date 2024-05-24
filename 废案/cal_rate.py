import time
import ovito.data
import numpy as np
import ovito.io
import matplotlib.pyplot as plt
from ovito.modifiers import CommonNeighborAnalysisModifier, SliceModifier, DislocationAnalysisModifier


def compute_dislocation(PATH) -> None:
    pipeline = ovito.io.import_file(PATH)
    dislocation = DislocationAnalysisModifier()
    pipeline.modifiers.append(dislocation)
    num_frames = pipeline.source.num_frames
    dislocation_data = np.zeros((num_frames, 8), dtype=float)
    for idx in range(num_frames):
        if idx == 0 and __name__ == '__main__':
            _start = time.time()

        data = pipeline.compute(idx)
        total_line_length = data.attributes['DislocationAnalysis.total_line_length']
        cell_volume = data.attributes['DislocationAnalysis.cell_volume']
        perfect_length = data.attributes['DislocationAnalysis.length.1/2<110>']
        shockley_length = data.attributes['DislocationAnalysis.length.1/6<112>']
        stair_rod_length = data.attributes['DislocationAnalysis.length.1/6<110>']
        hirth_length = data.attributes['DislocationAnalysis.length.1/3<100>']
        frank_length = data.attributes['DislocationAnalysis.length.1/3<111>']
        other_length = data.attributes['DislocationAnalysis.length.other']

        dislocation_data[idx, :] = np.array([total_line_length, cell_volume, perfect_length,
                                             shockley_length, stair_rod_length, hirth_length,
                                            frank_length, other_length])
        if idx == 0 and __name__ == '__main__':
            print(f"One Epoch cost:{time.time()-_start}")
    print("Finish compute")
    np.savetxt("dislocation_data.txt", dislocation_data, fmt='%d')

def main():

    compute_dislocation("D:/Atomsk/Model/合金拉伸/CoNiCr/剪切/test.xyz")

if __name__ == '__main__':
    main()
