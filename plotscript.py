import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

class Plotter:
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
    phis = np.stack([np.load(f'{fpath}_phis.npy') for fpath in filepaths], axis = 0)
    rms = np.stack([np.load(f'{fpath}_rms.npy') for fpath in filepaths], axis=0)


    def __init__(self):

    def phis_data_stack(self):



