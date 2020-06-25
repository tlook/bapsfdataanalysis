import numpy as np
from bapsflib import lapd

hconc = {
    100 : '03',
    90 : '09',
    80 : '06',
    70 : '11',
    60 : '12',
    50 : '05',
    40 : '13',
    30 : '14',
    20 : '07',
    10 : '08',
    0 : '04'
}
filenames = [f'{hconc[key]}_x_H{key}_D{100 - key}' for key in list(hconc.keys())]
filepaths = [f'/data/tlook/{fname}/{fname}' for fname in filenames]
for i, fname in enumerate(filenames):
    file = lapd.File(f'/data/BAPSF_Data/Multi_Ion_Transport/HD_April2019/{filenames[i]}.hdf5')
    voltage_top = file.read_data(3, 4)['signal']
    voltage_bot = file.read_data(3, 5)['signal']
    np.save(f'{filepaths[i]}_vtop.npy', voltage_top)
    np.save(f'{filepaths[i]}_vbot.npy', voltage_bot)
