def process_flucs(data):
    s = data[:, 1]
    s1 = savgol_filter(s, g.SAVGOL_WINDOW_LENGTH, 2)
    phi = s - s1
    return s1, phi


def extract_flucs(signals, locs, time_step):
    phi_file = f'{USER_DIR}{DATA_SRC_FILE}/{DATA_SRC_FILE}_phis.npy'
    try:
        phis = np.load(phi_file)
        print('loaded PHIS')
    except IOError:
        print("extracting Phis")
        phis = []
        for i, shots in enumerate(signals):
            arr = []
            print(f'extracting phi_{i}')
            for t, signal in enumerate(shots):
                arr.append((t*time_step, signal))
            plot_data = np.array(arr)
            # plot_and_save(f'raw_signal_{i}', locs[i//25], plot_data)
            trimmed_data = plot_data[:SIG_WINDOW_END]
            phis.append(process_flucs(locs[i//SHOTS], trimmed_data, i))
        phis = np.array(phis)
        np.save(phi_file, phis)
        print("phis saved")
    return phis


def fluc_analysis(phis, dt):
    spectra = []
    freqbin = rfftfreq(SIG_WINDOW_END, d=dt)
    print(freqbin.shape, freqbin.shape[0])
    for i, phi in enumerate(phis):
        phitilda = rfft(phi)
        spectra.append(np.square(np.absolute(phitilda)))
    avg_spec = np.average(np.array(spectra).reshape((POINTS, SHOTS, freqbin.shape[0])), axis=1)
    return avg_spec, freqbin