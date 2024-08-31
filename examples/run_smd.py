'''
Usage:
    mpirun -n 2 python run_smd.py
'''

from psana_wrapper import PsanaWrapperSmd, ImageRetrievalMode

# -- MPI (Optional)
from mpi4py import MPI
mpi_comm = MPI.COMM_WORLD
mpi_rank = mpi_comm.Get_rank()
mpi_size = mpi_comm.Get_size()
mpi_data_tag     = 11
mpi_request_tag  = 12
mpi_terminal_tag = 13

# -- Main
exp           = 'mfxl1027522'
run           = '26'
detector_name = 'epix10k2M'

smd_wrapper = PsanaWrapperSmd(
    exp           = exp,
    run           = run,
    detector_name = detector_name,
)

for idx, data in enumerate(smd_wrapper.iter_events(ImageRetrievalMode.image)):
    if idx > 10: break
    print(f"RANK={mpi_rank} | idx = {idx} | shape = {data.shape}")
