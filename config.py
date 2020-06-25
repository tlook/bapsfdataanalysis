from configparser import ConfigParser


class LoadConfig:
    def __init__(self, configfile):
        self.config = ConfigParser()
        self.config.read(configfile)
        # PATHS
        self.USER_DIR = self.config.get('PATHS', 'user_dir')
        self.PLOT_DIR = self.config.get('PATHS', 'plot_dir')
        self.DATA_SRC_DIR = self.config.get('PATHS', 'data_src_dir')
        self.DATA_SRC_FILE = self.config.get('PATHS', 'data_src_file')
        # BAPSFLIB SETTINGS
        self.CONTROLLERS = [self.config.get('BAPSFLIB', 'controllers')]
        self.SHOTS = self.config.getint('BAPSFLIB', 'shots')
        self.POINTS = self.config.getint('BAPSFLIB', 'points')
        self.BOARD = self.config.getint('BAPSFLIB', 'board')
        self.CHANNEL = self.config.getint('BAPSFLIB', 'channel')
        self.TIME_STEPS = self.config.getint('BAPSFLIB', 'time_steps')
        # ANALYZER SETTINGS
        self.TIME_WINDOW_START = self.config.getint('ANALYSIS', 'time_window_start')
        self.TIME_WINDOW_END = self.config.getint('ANALYSIS', 'time_window_end')
        self.SAVGOL_WINDOW_LENGTH = self.config.getint('ANALYSIS', 'savgol_window_length')
        return


isat = np.stack(
    [np.average(
        np.average(np.load(f'{fpath}').reshape(2020, 20, 65536), axis=1)[:,18750:28125],axis=1) for fpath in filepath2])
