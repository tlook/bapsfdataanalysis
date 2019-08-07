import os
import numpy as np
import globalvars as g

import numpy as np
from numpy.fft import rfft, rfftfreq
from scipy.signal import savgol_filter
from configparser import ConfigParser

# User's data directory on Midas

def main():
    os.makedirs(f'{g.USER_DIR}{g.DATA_SRC_FILE}', exist_ok=True)
    # Extract data from HDF5 files
    signals, xyzs, time_step = extract_raw_data(g.BOARD, g.CHANNEL)
    # Create directory structure
    xyz1 = xyzs[::g.SHOTS]
    locs = []
    for i in range(g.POINTS):
        loc = location(xyz1[i, 0], xyz1[i, 1])
        os.makedirs(save_dir(loc), exist_ok=True)
        locs.append(loc)
    # Make plots of the raw signals or spectrum
    phis = extract_flucs(signals, locs, time_step)
    avg_spec_data, freqbin = fluc_analysis(phis, time_step)
    for i, data in enumerate(avg_spec_data):
        plot_spectrum(freqbin, data, locs[i])
    # Make plots of signal averaged over shots at a spot
    plot_averages(signals, xyz1, locs, time_step)


if __name__ == '__main__':
    main()
