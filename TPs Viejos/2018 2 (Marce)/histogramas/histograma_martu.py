# coding=utf-8
from computar_maximos import computar_notch
from read_spice_montecarlo import read_file_spice
from make_histogram import make_histogram
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Arial']})
#rc('text', usetex=True)

data = read_file_spice("EJ4/simulaciones/UNIVERSAL_ETAPA2_MODIFICADO.txt")

arr = {"notch_f": [], "min": [], "bw": []}

for i in range(len(data)):
    info = computar_notch(data[i])

    arr["notch_f"].append(info["notch_f"])
    arr["min"].append(info["min"])
    arr["bw"].append(info["f2"]-info["f1"])

#print(arr)

make_histogram(variable="Notch frecuency",
               unidad="Hz",
               data=arr["notch_f"],
               filename="histograma_martu_notch_frecuency.png",
               bar_width=50741-50225)

make_histogram(variable="Notch depth",
               unidad="dB",
               data=arr["min"],
               filename="histograma_martu_notch_depth.png",
               bar_width=6)

make_histogram(variable="Notch bandwidth",
               unidad="Hz",
               data=arr["bw"],
               filename="histograma_martu_notch_bw.png",
               bar_width=40169-39783)

