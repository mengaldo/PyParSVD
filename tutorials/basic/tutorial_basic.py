import os
import sys
import time
import numpy as np

# Current, parent and file paths
CWD = os.getcwd()
CF  = os.path.realpath(__file__)
CFD = os.path.dirname(CF)

# Import library specific modules
sys.path.append(os.path.join("../../"))
from pyparsvd.parsvd_serial   import ParSVD_Serial
from pyparsvd.parsvd_parallel import ParSVD_Parallel



# Construct SVD objects
SerSVD = ParSVD_Serial(K=10, ff=1.0)
ParSVD = ParSVD_Parallel(K=10, ff=1.0, low_rank=True)

# Path to data
path = os.path.join(CFD, './data/')

# Serial data
initial_data_ser = np.load(os.path.join(path, 'Batch_0_data.npy'))
new_data_ser = np.load(os.path.join(path, 'Batch_1_data.npy'))
newer_data_ser = np.load(os.path.join(path, 'Batch_2_data.npy'))
newest_data_ser = np.load(os.path.join(path, 'Batch_3_data.npy'))

# Parallel data
initial_data_par = np.load(os.path.join(path, 'points_rank_' + str(ParSVD.rank) + '_batch_0.npy'))
new_data_par = np.load(os.path.join(path, 'points_rank_' + str(ParSVD.rank) + '_batch_1.npy'))
newer_data_par = np.load(os.path.join(path, 'points_rank_' + str(ParSVD.rank) + '_batch_2.npy'))
newest_data_par = np.load(os.path.join(path, 'points_rank_' + str(ParSVD.rank) + '_batch_3.npy'))

# Do first modal decomposition -- Serial
s = time.time()
SerSVD.initialize(initial_data_ser)

# Incorporate new data -- Serial
SerSVD.incorporate_data(new_data_ser)
SerSVD.incorporate_data(newer_data_ser)
SerSVD.incorporate_data(newest_data_ser)
if SerSVD.rank == 0: print('Elapsed time SERIAL: ', time.time() - s, 's.')

# Do first modal decomposition -- Parallel
s = time.time()
ParSVD.initialize(initial_data_par)

# Incorporate new data -- Parallel
ParSVD.incorporate_data(new_data_par)
ParSVD.incorporate_data(newer_data_par)
ParSVD.incorporate_data(newest_data_par)
if ParSVD.rank == 0: print('Elapsed time PARALLEL: ', time.time() - s, 's.')

# Basic postprocessing
if ParSVD.rank == 0:

	# Save results
	SerSVD.save()
	ParSVD.save()

	# Visualize singular values and modes modes
	SerSVD.plot_singular_values(filename='serial_sv.png')
	ParSVD.plot_singular_values(filename='parallel_sv.png')
	SerSVD.plot_1D_modes(filename='serial_1d_mode0.png')
	ParSVD.plot_1D_modes(filename='parallel_1d_mode0.png')
	SerSVD.plot_1D_modes(filename='serial_1d_mode2.png', idxs=[2])
	ParSVD.plot_1D_modes(filename='parallel_1d_mode2.png', idxs=[2])
