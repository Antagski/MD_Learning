"""
#########################################################
The multiprocessing module needs to send the input      #
parameters and the return value of our worker function  #
across process boundaries. This happens via Python’s    #
pickle mechanism, which is something most OVITO objects #
do not support yet. Things like a DataCollection and    #
its contents, or a Pipeline and its modifiers cannot    #
be transmitted from the main program to the parallel    #
worker function. We therefore need to restrict ourselves#
to simple Python values, objects, or NumPy arrays that  #
can be pickled.                                         #
#########################################################
"""

# This configuration flag enables the use of the Python multiprocessing module.
# Set it to false to switch back to conventional for-loop processing (included for comparison).
use_multiprocessing = True

if use_multiprocessing:
    # Disable internal parallelization of OVITO's pipeline system, which otherwise would perform certain
    # computations using all available processor cores. Setting the environment variable OVITO_THREAD_COUNT=1
    # must be done BEFORE importing the ovito module and will restrict OVITO to a single CPU core per process.
    import os
    os.environ["OVITO_THREAD_COUNT"] = "4"

from ovito.io import *
from ovito.modifiers import *
import numpy
import ovito.data
import numpy as np
import ovito.io
import matplotlib.pyplot as plt
import PySide6.QtWidgets
from functools import partial

# Set up the OVITO data pipeline for performing some heavy computations for each trajectory frame.
# Keep in mind that this initialization code gets executed by EVERY worker process in the multiprocessing pool.
# So we should only prepare but not carry out any expensive operations here.

PATH = 'D:/Atomsk/Model/合金拉伸/CoNiCr/拉伸/Outputs/30_60_240/CoCrNiTension.xyz'
pipeline = import_file(PATH)
print("Finish read_file")
dislocation = DislocationAnalysisModifier()
pipeline.modifiers.append(dislocation)
# dislocation_data = np.zeros((num_frames - 1, 8))

# Define the worker function which gets called for every trajectory frame. It evaluates the pipeline
# at the requested simulation time and returns the computed results for that frame back to the caller.
#
# IMPORTANT: The function may only return regular Python objects but not OVITO objects
# such as DataCollection or Property. That's because OVITO objects do not currently support pickling,
# which means they cannot be sent back to the main program across process boundaries.
#
# In this simple example, the return value is a simple scalar (a global attribute) computed per frame.
# Note that it is possible to return NumPy arrays, which includes NumPy views of OVITO property arrays.
# Thus, to return the cluster assignment of each atom computed by the ClusterAnalysisModifier
# we could write:
#
#    return data.particles['Cluster'][...]
#
def process_frame(pipeline, frame):

    data = pipeline.compute(frame)

    total_line_length = data.attributes['DislocationAnalysis.total_line_length']
    cell_volume = data.attributes['DislocationAnalysis.cell_volume']
    perfect_length = data.attributes['DislocationAnalysis.length.1/2<110>']
    shockley_length = data.attributes['DislocationAnalysis.length.1/6<112>']
    stair_rod_length = data.attributes['DislocationAnalysis.length.1/6<110>']
    hirth_length = data.attributes['DislocationAnalysis.length.1/3<100>']
    frank_length = data.attributes['DislocationAnalysis.length.1/3<111>']
    other_length = data.attributes['DislocationAnalysis.length.other']

    dislocation_data = np.array([total_line_length, cell_volume, perfect_length,
                                         shockley_length, shockley_length, hirth_length,
                                         frank_length, other_length])
    return dislocation_data

# Main program entry point:
if __name__ == '__main__':

    # Measure time for benchmarking purposes.
    from time import time
    t_start = time()




    # num_frames = pipeline.source.num_frames

    if use_multiprocessing:

        # Force "spawn" start method on all platforms, because OVITO is not compatible with "fork" method.
        import multiprocessing as mp
        mp.set_start_method('spawn')

        # Create a pool of processes which will process the trajectory frames in parallel.
        with mp.Pool(None) as pool:
            partial_func = partial(process_frame, pipeline)
            results = list(pool.imap(partial_func, range(pipeline.source.num_frames)))
            # results = list(pool.imap(process_frame, range(pipeline.source.num_frames)))

    else:

        # Conventional for-loop iterating over all frames of the trajectory and processing one by one.
        results = [process_frame(frame) for frame in range(pipeline.source.num_frames)]

    t_end = time()

    print(f"Computation took {t_end - t_start} seconds")