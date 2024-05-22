import multiprocessing
import os
import time
import numpy
import ovito.data
import numpy as np
import ovito.io
from ovito.modifiers import CommonNeighborAnalysisModifier, SliceModifier, DislocationAnalysisModifier


def read_file(PATH) -> ovito.pipeline.Pipeline:
    pipeline = ovito.io.import_file(PATH)
    # print("Finish read_file")
    return pipeline

# 定义任务函数，这里假设task函数接收文件路径并处理文件
def task(file_path):
    pipeline = read_file(file_path)

    dislocation = DislocationAnalysisModifier()
    pipeline.modifiers.append(dislocation)
    num_frames = pipeline.source.num_frames

    dislocation_data = np.zeros((num_frames, 8), dtype=float)  # 修正数组大小
    for idx in range(num_frames):
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

    np.savetxt(f"{os.path.basename(file_path).split(".")[0]}.txt", dislocation_data, fmt='%d')
    return f"Processed {file_path}"

def main(directory, max_workers):
    # 获取所有数据文件的路径
    files = [os.path.join(directory, f).replace('\\', '/') for f in os.listdir(directory) if f.endswith('.xyz')]

    # 使用 multiprocessing.Pool 来并行执行任务
    with multiprocessing.Pool(processes=max_workers) as pool:
        results = pool.map(task, files)
        for result in results:
            print(result)

if __name__ == "__main__":
    # 设定数据文件夹路径
    directory = 'D:/Atomsk/TEMP'
    # 设定进程池中最大进程数
    max_workers = 16

    start_time = time.time()
    main(directory, max_workers)
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")
