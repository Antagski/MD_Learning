import time
import ovito.data
import numpy as np
import ovito.io
import ovito.modifiers


def compute_dislocation(PATH: str) -> None:
    pipeline = ovito.io.import_file(PATH)
    dislocation = ovito.modifiers.DislocationAnalysisModifier()
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
            print(f"DXA: One Epoch cost:{time.time()-_start}")

    print("The process of calculating DXA is completed")
    np.savetxt("dislocation_data.txt", dislocation_data, fmt='%d')


def identify_phase(PATH: str):
    pipeline = ovito.io.import_file(PATH)
    cna = ovito.modifiers.CommonNeighborAnalysisModifier()
    pipeline.modifiers.append(cna)
    num_frames = pipeline.source.num_frames

    counts = np.zeros((num_frames, 5))

    for idx in range(num_frames):
        if idx == 0 and __name__ == '__main__':
            _start = time.time()

        data = pipeline.compute(idx)
        structure_types = data.particles['Structure Type']
        _counts = _get_structure_type_rate(structure_types)
        counts[idx, :] = _counts

        if idx == 0 and __name__ == '__main__':
            print(f"CNA: One Epoch cost:{time.time()-_start}")

    print("The process of calculating CNA is completed")
    np.savetxt("phase_data.txt", counts, fmt='%d')


def _get_structure_type_rate(structure_types: ovito.data.ParticleType) -> np.array:
    data = np.array(structure_types)
    _counts = np.zeros((1, 5))
    for type in range(4):
        _counts[0, [type]] = np.sum(data == type)
    return _counts


def identify_planar_fault(PATH: str):
    pipeline = ovito.io.import_file(PATH)
    ptm = ovito.modifiers.PolyhedralTemplateMatchingModifier(output_orientation=True,
                                                             output_interatomic_distance=True)
    ifpf = ovito.modifiers.IdentifyFCCPlanarFaultsModifier()
    pipeline.modifiers.append(ptm)
    pipeline.modifiers.append(ifpf)

    num_frames = pipeline.source.num_frames

    counts = np.zeros((num_frames, 5))
    areas = np.zeros((num_frames, 5))

    for idx in range(num_frames):
        if idx == 0 and __name__ == '__main__':
            _start = time.time()

        data = pipeline.compute(idx)
        table = data.tables['planar_faults']
        num_atoms_NONHCP = table['Atom Count'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.NONHCP]
        num_atoms_OTHER = table['Atom Count'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.OTHER]
        num_atoms_ISF = table['Atom Count'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.ISF]
        num_atoms_TWIN = table['Atom Count'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.TWIN]
        num_atoms_MULTI = table['Atom Count'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.MULTI]

        area_NONHCP = table['Estimated Area'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.NONHCP]
        area_OTHER = table['Estimated Area'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.OTHER]
        area_ISF = table['Estimated Area'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.ISF]
        area_TWIN = table['Estimated Area'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.TWIN]
        area_MULTI = table['Estimated Area'][ovito.modifiers.IdentifyFCCPlanarFaultsModifier.Types.MULTI]

        counts[idx, :] = np.array([
            num_atoms_NONHCP, num_atoms_OTHER, num_atoms_ISF, num_atoms_TWIN, num_atoms_MULTI
        ])

        areas[idx, :] = np.array([
            area_NONHCP, area_OTHER, area_ISF, area_TWIN, area_MULTI
        ])

        if idx == 0 and __name__ == '__main__':
            print(f"FCCPlanarFault: One Epoch cost:{time.time()-_start}")

    print("The process of calculating FCCPlanarFault is completed")
    np.savetxt("PF_counts_data.txt", counts, fmt='%d')
    np.savetxt("PF_areas_data.txt", areas, fmt='%d')


def main():
    # PATH = "D:/Atomsk/Model/合金拉伸/CoNiCr/剪切/test.xyz"
    PATH = "E:/Server/13nm/13nm.xyz"
    identify_planar_fault(PATH)
    compute_dislocation(PATH)
    identify_phase(PATH)


if __name__ == "__main__":
    main()