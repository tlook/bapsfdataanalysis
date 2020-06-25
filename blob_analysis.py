from analysis import IsatAnalysis


def main():
    """
    Main program - Load or extract data from HDF5 files (and create directory structure if necessary)
    Saves extracted data and computes quantities for plotting (details in respective functions/methods)
    Creates and saves plots (probably as specified in config file.)
    :return:
    """
    configs = [f'/data/tlook/scripts/bapsfda/scripts/config{i}.ini' for i in range(11)]
    for config in configs:
        IsatAnalysis(config)
    return


if __name__ == '__main__':
    main()
