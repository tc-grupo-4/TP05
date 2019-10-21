# coding=utf-8

from scipy import signal
from math import *
from random import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datacursor_easy
import read_spice
import numpy as np
import read_csv
import read_xls
import transfer

f_range = np.logspace(2, 3, 10000)
w_range = [2 * pi * i for i in f_range]


def plot_mediciones(mode, mediciones_filename, spice_filename, output_filename, my_tf , plantillaPoints = None, zin=False):

    fig, ax1 = plt.subplots()
    patches = []

    w, mag, pha = signal.bode(my_tf, w_range)

    f = [i / 2 / pi for i in w]
    #for j in range(len(pha)):
         # if pha[j] < -180:
         #     pha[j] += 360
        #pha[j] -= 180
    if mode == "mag":
        if zin:
            for i in range(len(mag)):
                mag[i] = 10**(mag[i]/20.0)/1000.0
        ax1.semilogx(f, mag, "green")
    else:
        ax1.semilogx(f, pha, "green")

    patches.append(mpatches.Patch(color="green", label="Teórico"))

    if spice_filename != "":
        data_spice = read_spice.read_file_spice("Simulacion/" + spice_filename)

        if mode == "mag":
            if zin:
                for i in range(len(data_spice["abs"])):
                    data_spice["abs"][i] = 10 ** (data_spice["abs"][i]/20.0)/1000.0
                ax1.semilogx(data_spice["f"], data_spice["abs"], "red")
            else:
                ax1.semilogx(data_spice["f"], data_spice["abs"], "red")
        else:
            for i in range(len(data_spice["pha"])):
                if data_spice["pha"][i] > 0:
                    data_spice["pha"][i] -= 360.0
                data_spice["pha"][i] += 180
                # pass
            ax1.semilogx(data_spice["f"], data_spice["pha"], "red")

        patches.append(mpatches.Patch(color="red", label="Simulación"))

    if mediciones_filename != "":
        data_mediciones = read_xls.read_excel_data("Mediciones/"+mediciones_filename)

        if mode == "mag":
            if not zin:
                ax1.semilogx(data_mediciones["Freq"], data_mediciones["Ratio"], "blue")
            else:
                for i in range(len(data_mediciones["ZIN ABS COPY"])):
                    data_mediciones["ZIN ABS COPY"][i] = data_mediciones["ZIN ABS COPY"][i] / 1000.0
                ax1.semilogx(data_mediciones["Freq"], data_mediciones["ZIN ABS COPY"], "blue")
        else:
            if zin:
                # for i in range(len(data_mediciones["ZIN PHA COPY"])):
                #     data_mediciones["ZIN PHA COPY"][i] = data_mediciones["ZIN PHA COPY"][i] - 180
                ax1.semilogx(data_mediciones["Freq"], data_mediciones["ZIN PHA COPY"], "blue")
            else:
                # for i in range(len( data_mediciones["Pha"])):
                #     data_mediciones["Pha"][i] -= 180
                ax1.semilogx(data_mediciones["Freq"], data_mediciones["Pha"], "blue")

        patches.append(mpatches.Patch(color="blue", label="Mediciones"))

    if plantillaPoints:
        mag_new = [i for i in plantillaPoints[1]]

        ax1.semilogx(plantillaPoints[0], mag_new, "black")


    plt.legend(handles=patches)
    if zin:
        datacursor_easy.add_legend_zin(mode, ax1, plt)

        datacursor_easy.make_datacursor_zin(mode, "graficos_express/output/" + output_filename, plt, fig, ax1)
    else:
        datacursor_easy.add_legend(mode, ax1, plt)

        datacursor_easy.make_datacursor(mode, "graficos_express/output/" + output_filename, plt, fig)

k = 1e3

plantilla_points = [
    [34.25*k, 34.25*k, 37.84*k, 37.84*k],
    [-30, -3, -3, -30]
]


# plot_mediciones(mode="mag",
#                 mediciones_filename="Bode.xlsx",
#                 spice_filename="Bode.txt",
#                 output_filename="H_mag.png",
#                 my_tf=transfer.tf,
#                 plantillaPoints=plantilla_points
# )
# plot_mediciones(mode="pha",
#                 mediciones_filename="Bode.xlsx",
#                 spice_filename="Bode.txt",
#                 output_filename="H_pha.png",
#                 my_tf=transfer.tf
# )
plot_mediciones(mode="mag",
                mediciones_filename="Zin.xlsx",
                spice_filename="Zin.txt",
                output_filename="Zin_mag.png",
                my_tf=transfer.tfZin,
                zin=True
)
plot_mediciones(mode="pha",
                mediciones_filename="Zin.xlsx",
                spice_filename="Zin.txt",
                output_filename="Zin_pha.png",
                my_tf=transfer.tfZin,
                zin=True
)