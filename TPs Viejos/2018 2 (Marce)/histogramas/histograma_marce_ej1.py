# coding=utf-8

from computar_maximos import conseguir_fp
from read_spice_montecarlo import read_file_spice
import seaborn as sns
import matplotlib.pyplot as plt
from make_histogram import make_histogram
from computar_maximos import computar_maximos_bp

data = read_file_spice("EJ1/Circuito con Bessel/Simulacion/BodeMontecarlo.txt")


arr = []
for i in range(len(data)):
    act = conseguir_fp(data[i], -3)

    arr.append(act)

make_histogram(variable="Frecuencia de corte",
               unidad="Hz",
               data=arr,
               filename="histograma_marce_ej1_bessel.png",
               bar_width=570.619-548.393)


data = read_file_spice("EJ1/Circuito con Legendre/Simulacion/BodeMontecarlo.txt")

arr = []

for i in range(len(data)):
    act = conseguir_fp(data[i], -3)
    arr.append(act)

make_histogram(variable="Frecuencia de corte",
               unidad="Hz",
               data=arr,
               filename="histograma_marce_ej1_legendre.png",
               bar_width=24369-23171)


data = read_file_spice("EJ2/Simulacion/BodeMontecarlo.txt")

arr = {"f1": [], "f2": []}

for i in range(len(data)):
    info = computar_maximos_bp(data[i])

    arr["f1"].append(info["f1"])
    arr["f2"].append(info["f2"])


make_histogram(variable="Frecuencia 1 de 3db",
               unidad="Hz",
               data=arr["f1"],
               filename="histograma_marce_EJ2_f13db.png",
               bar_width=33105-31841)


make_histogram(variable="Frecuencia 2 de 3db",
               unidad="Hz",
               data=arr["f2"],
               filename="histograma_marce_EJ2_f23db.png",
               bar_width=38375-37786)


