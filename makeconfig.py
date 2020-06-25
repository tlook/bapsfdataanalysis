import configparser

config = configparser.ConfigParser()
config.read('config.ini')
config.add_section('PATHS')
config.set('PATHS', 'USER_DIR', '/data/tlook/')
config.set('PATHS', 'PLOT_DIR', 'plots/')
config.set('PATHS', 'DATA_SRC_DIR', '/data/BAPSF_Data/Multi_Ion_Transport/HD_April2019/')
config.set('PATHS', 'DATA_SRC_FILE', '03_x_H100_D0')
config.add_section('BAPSFLIB')
config.set('BAPSFLIB', 'CONTROLLERS', '6K Compumotor')
config.set('BAPSFLIB', 'SHOTS', '20')
config.set('BAPSFLIB', 'POINTS', '101')
config.set('BAPSFLIB', 'BOARD', '3')
config.set('BAPSFLIB', 'CHANNEL', '3')
config.set('BAPSFLIB', 'TIME_STEPS', '65536')
config.add_section('ANALYSIS')
config.set('ANALYSIS', 'TIME_WINDOW_START', '18750')
config.set('ANALYSIS', 'TIME_WINDOW_END', '28125')
config.set('ANALYSIS', 'SAVGOL_WINDOW_LENGTH', '28125')

with open('config.ini', 'w') as f:
    config.write(f)
