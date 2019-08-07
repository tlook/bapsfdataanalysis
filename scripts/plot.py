import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scripts.utils import save_name
import numpy as np
import globalvars as g


def plot_spectrum(freqbin, norm_spec, loc):
    plt.figure()
    plt.subplot(111)
    # plt.xlim(0, 2e5)
    # plt.ylim(10e-7, 10e2)
    plt.yscale("log")
    plt.plot(np.log10(freqbin), norm_spec, linewidth=0.2)
    plt.savefig(save_name('spectrum', loc))
    plt.close()
    return


def plot_fluc(t, s, s1, phi, loc):
    plt.figure()
    plt.subplot(111)
    plt.plot(t, s, linewidth=.1)
    plt.plot(t, s1, color='red')
    plt.savefig(save_name(f'savgol_{n}', loc))
    plt.close()
    plt.figure()
    plt.subplot(111)
    plt.plot(t, phi, color='red')
    plt.savefig(save_name(f'extracted_signal_{n}', loc))
    plt.close()
    return


def plot_averages(signals, xyzs, locs, time_step):
    avg_signal = np.average(signals.reshape((g.POINTS, g.SHOTS, g.TIME_STEPS)), axis=1)
    for i, spots in enumerate(avg_signal):
        arr = []
        for t, signal in enumerate(spots):
            arr.append((t*time_step, signal))
        plot_data = np.array(arr)
        plot_and_save('avg_signal', locs[i], plot_data)
    avg_signal_top = np.average(avg_signal[:, g.TIME_WINDOW_START:g.TIME_WINDOW_END], axis=1)
    data = np.column_stack((xyzs[:, 0], avg_signal_top))
    plt.figure()
    plt.subplot(111)
    plt.plot(data[:, 0], data[:, 1], linewidth=.3)
    plt.savefig(f'{g.USER_DIR}{g.DATA_SRC_FILE}/{g.PLOT_DIR}avgsig_v_x.pdf')
    plt.close()
    # plot_tricon(x, y, avg_signal_top)
    return

def plot_and_save(filename, loc, data):
    plt.figure()
    plt.subplot(111)
    plt.plot(data[:, 0], data[:, 1], linewidth=.3)
    plt.savefig(save_name(filename, loc))
    plt.close()


def plot_tricon(x, y, z):
    ngridx = 41
    ngridy = 41
    xi = np.linspace(-10, 10, ngridx)
    yi = np.linspace(-10, 10, ngridy)

    triang = tri.Triangulation(x, y)
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    plt.figure()
    ax1 = plt.subplot(111)
    ax1.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
    cntr1 = ax1.contourf(xi, yi, zi, levels=14, cmap="RdBu_r")
    plt.colorbar(cntr1, ax=ax1)
    # ax1.plot(x, y, 'ko', ms=3)
    ax1.set(xlim=(-10, 10), ylim=(-10, 10))
    ax1.set_title('grad and contour')
    plt.savefig('testgradcont.pdf')
    plt.close()

    plt.figure()
    ax2 = plt.subplot(111)
    ax2.tricontour(x, y, z, levels=14, linewidths=0.5, colors='k')
    cntr2 = ax2.tricontourf(x, y, z, levels=14, cmap="RdBu_r")
    plt.colorbar(cntr2, ax=ax2)
    # ax2.plot(x, y, 'ko', ms=3)
    ax2.set(xlim=(-10, 10), ylim=(-10, 10))
    ax2.set_title('tricontour')
    plt.savefig('testtricont.pdf')
    plt.close()
    return
