import numpy as np
import globalvars as g
from bapsflib import lapd


def extract_raw_data():
    name_temp = f'{g.USER_DIR}{g.DATA_SRC_FILE}/{g.DATA_SRC_FILE}-b{g.BOARD}_c{g.CHANNEL}'
    signal_file = f'{name_temp}_signals.npy'
    xyz_file = f'{name_temp}_xyz.npy'
    dt_file = f'{name_temp}_dt.npy'
    try:
        signal_shots = np.load(signal_file)
        xyz_shots = np.load(xyz_file)
        dt = np.load(dt_file)
        print('Successfully Loaded Files.')
    except IOError:
        print('Could not load files. Extracting data from source.')
        file = lapd.File(f'{g.DATA_SRC_DIR}{g.DATA_SRC_FILE}.hdf5')
        data = file.read_data(g.BOARD, g.CHANNEL, add_controls=g.CONTROLLERS)
        signal_shots = data['signal']
        xyz_shots = data['xyz']
        dt = data.dt.value
        print('Data loaded. Saving to disk...')
        np.save(signal_file, signal_shots)
        np.save(xyz_file, xyz_shots)
        np.save(dt_file, dt)
        print('Data saved.')
    return signal_shots, xyz_shots.round(2), dt


def location(x, y):
    return f'x[{x:.2f}]_y[{y:.2f}]'


def save_dir(loc):
    return f'{g.USER_DIR}{g.DATA_SRC_FILE}/{g.PLOT_DIR}{loc}/'


def save_name(filename, loc):
    return f'{save_dir(loc)}{filename}-{loc}.pdf'
