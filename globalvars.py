from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# PATHS
USER_DIR = config.get('PATH', 'user_dir')
PLOT_DIR = config.get('PATH', 'plot_dir')
DATA_SRC_DIR = config.get('PATH', 'data_src_file')
DATA_SRC_FILE = config.get('PATH', 'data_src_file')

# BAPSFLIB SETTINGS
CONTROLLERS = [config.get('BAPSFLIB', 'controllers')]
SHOTS = config.getint('BAPSFLIB', 'shots')
POINTS = config.getint('BAPSFLIB', 'points')
BOARD = config.getint('BAPSFLIB', 'board')
CHANNEL = config.getint('BAPSFLIB', 'channel')
TIME_STEPS = config.getint('BAPSFLIB', 'time_steps')

# ANALYZER SETTINGS
TIME_WINDOW_START = config.getint('ANALYSIS', 'time_window_start')
TIME_WINDOW_END = config.getint('ANALYSIS', 'time_window_end')
SAVGOL_WINDOW_LENGTH = config.getint('ANALYSIS', 'savgol_window_length')
