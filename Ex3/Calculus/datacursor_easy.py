# coding=utf-8

from mpldatacursor import datacursor


def make_datacursor_general(x1, u1, filename, my_plt, ax1):
    datacursor(display='multiple', tolerance=0,
               formatter=(str(x1)+" ("+str(u1) + "): {x:.3e}  Hz \n").format,
               draggable=True)

    my_plt.gca().minorticks_on()
    my_plt.gca().grid(which='major', linestyle='-', linewidth=0.3, color='black')
    my_plt.gca().grid(which='minor', linestyle=':', linewidth=0.1, color='black')

    # my_plt.show()
    # input("Press Enter ")

    my_plt.gcf().savefig(filename, dpi=300)

    my_plt.cla()
    my_plt.close()


def make_datacursor(mode, filename, my_plt , fig):
    if mode == "mag":
        datacursor(display='multiple', tolerance=10, formatter="Freq: {x:.3e}  Hz \nAmp:{y:.1f} Db".format,
                   draggable=True)
    else:
        datacursor(display='multiple', tolerance=10, formatter="Freq: {x:.3e}  Hz \nFase:{y:.1f} grados".format,
                   draggable=True)

    my_plt.show()
    input("Press Enter ")

    fig.savefig(filename, dpi=300)
    my_plt.cla()
    my_plt.close()


def add_legend(my_mode, ax, my_plt):

    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth=0.3, color='black')
    ax.grid(which='minor', linestyle=':', linewidth=0.1, color='black')

    my_plt.xlabel("Frecuencia (Hz)")
    if my_mode == "mag":
        my_plt.ylabel("Amplitud (dB)")
    else:
        my_plt.ylabel("Fase (grados)")



def add_legend_zin(mode, ax, plt):

    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth=0.3, color='black')
    ax.grid(which='minor', linestyle=':', linewidth=0.1, color='black')

    plt.xlabel("Frecuencia (Hz)")
    if mode == "mag":
        plt.ylabel("Impedancia (K $\Omega$)")
    else:
        plt.ylabel("Fase (grados)")


def make_datacursor_zin(mode, filename,my_plt , fig, ax):
    add_legend_zin(mode, ax, my_plt)

    if mode == "mag":
        datacursor(display='multiple', tolerance=10, formatter="Freq: {x:.3e}  Hz \nZin:{y:.1f} K $\Omega$".format,
                   draggable=True)
    else:
        datacursor(display='multiple', tolerance=10, formatter="Freq: {x:.3e}  Hz \nFase:{y:.1f} grados".format,
                   draggable=True)

    my_plt.show()
    input("Press Enter ")

    fig.savefig(filename, dpi=300)
    my_plt.cla()
    my_plt.close()

