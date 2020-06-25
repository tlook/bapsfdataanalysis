import numpy as np
import os
from bapsflib import lapd
from config import LoadConfig
from numpy.fft import rfft, rfftfreq
from scipy.signal import savgol_filter


class IsatAnalysis:
    def __init__(self, configfile):
        self.c = LoadConfig(configfile)
        print(f'Loaded config: {configfile}')
        self.DATA_PATH_TEMP = f'{self.c.USER_DIR}{self.c.DATA_SRC_FILE}/{self.c.DATA_SRC_FILE}'
        self.RAW_SIG_PLOT_DATA_FILE = f'{self.DATA_PATH_TEMP}_raw_sigs.npy'
        self.FREQ_BIN_FILE = f'{self.DATA_PATH_TEMP}_freq_bin.npy'
        self.AVG_SPEC_FILE = f'{self.DATA_PATH_TEMP}_avg_spec.npy'
        self.PHI_FILE = f'{self.DATA_PATH_TEMP}_phis.npy'
        self.RMS_FILE = f'{self.DATA_PATH_TEMP}_rms.npy'
        self.S1_FILE = f'{self.DATA_PATH_TEMP}_s1s.npy'
        os.makedirs(f'{self.c.USER_DIR}{self.c.DATA_SRC_FILE}', exist_ok=True)
        self.signals, self.xyzs, self.t, self.dt = self.extract_raw_data()
        self.locs = np.array([self.location(xyz[0], xyz[1]) for xyz in self.xyzs])
        print('Making directory structure...')
        for loc in self.locs:
            os.makedirs(self.save_dir(loc), exist_ok=True)
        print('Directories made')
        print('Loading Phis...')
        self.phis, self.s1s = self.extract_flucs()
        print('Loading spec')
        self.avg_spec, self.freq_bin = self.fluc_analysis()
        print('Loading rms')
        self.rms = self.rms_analysis()
        print(f'completed extracting data for self.c.DATA_SRC_FILE')

    def extract_raw_data(self):
        '''
        attempt to open extracted data and if this fails, extract and save the data.
        :return:
        '''
        name_temp = f'{self.c.USER_DIR}{self.c.DATA_SRC_FILE}/{self.c.DATA_SRC_FILE}-b{self.c.BOARD}_c{self.c.CHANNEL}'
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
            file = lapd.File(f'{self.c.DATA_SRC_DIR}{self.c.DATA_SRC_FILE}.hdf5')
            data = file.read_data(self.c.BOARD, self.c.CHANNEL, add_controls=self.c.CONTROLLERS)
            signal_shots = data['signal']
            xyz_shots = data['xyz'][::self.c.SHOTS].round(2)
            dt = data.dt.value
            print('Data loaded. Saving to disk...')
            np.save(signal_file, signal_shots)
            np.save(xyz_file, xyz_shots)
            np.save(dt_file, dt)
            print('Data saved.')
        t = np.array([dt * i for i in range(self.c.TIME_STEPS)])
        return signal_shots, xyz_shots, t, dt

    def extract_flucs(self):
        ss = self.signals[:, :self.c.TIME_WINDOW_END]
        try:
            phis = np.load(self.PHI_FILE)
            s1s = self.smooth(ss)
            print('loaded PHIS')
        except IOError:
            print("extracting phis")
            s1s = self.smooth(ss)
            phis = ss - s1s
            np.save(self.PHI_FILE, phis)
        return phis, s1s

    def smooth(self, ss):
        try:
            s1s = np.load(self.S1_FILE)
        except IOError:
            s1s = np.array([savgol_filter(s, self.c.SAVGOL_WINDOW_LENGTH, 2) for s in ss])
            np.save(self.S1_FILE, s1s)
        return s1s

    def fluc_analysis(self):
        try:
            freq_bin = np.load(self.FREQ_BIN_FILE)
            avg_spec = np.load(self.AVG_SPEC_FILE)
        except IOError:
            phitildes = np.array([rfft(phi) for phi in self.phis])
            spectra = np.array([self.abs_sq(phitilde) for phitilde in phitildes])
            freq_bin = rfftfreq(self.c.TIME_WINDOW_END, d=self.dt)
            avg_spec = np.average(np.array(spectra).reshape((self.c.POINTS, self.c.SHOTS, freq_bin.shape[0])), axis=1)
            np.save(self.FREQ_BIN_FILE, freq_bin)
            np.save(self.AVG_SPEC_FILE, avg_spec)
        return avg_spec, freq_bin

    def rms_analysis(self):
        try:
            rms = np.load(self.RMS_FILE)
        except IOError:
            rms = np.average(np.std(self.phis, axis=1).reshape((101, 20)), axis=1)
            np.save(self.RMS_FILE, rms)
        return rms

    def abs_sq(self, x):
        return np.square(np.absolute(x))

    def location(self, x, y):
        return f'x[{x:.2f}]_y[{y:.2f}]'

    def save_dir(self, loc):
        return f'{self.c.USER_DIR}{self.c.DATA_SRC_FILE}/{self.c.PLOT_DIR}{loc}/'

    def save_name(self, filename, loc):
        return f'{self.save_dir(loc)}{filename}-{loc}.pdf'
