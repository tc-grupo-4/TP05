# coding=utf-8

from computar_maximos import conseguir_fp
from read_spice_montecarlo import read_file_spice
import seaborn as sns
import matplotlib.pyplot as plt

data = read_file_spice("EJ1/Circuito con Legendre/Simulacion/BodeMontecarlo.txt")


arr = []

for i in range(len(data)):
    act = conseguir_fp(data[i], -3)

    arr.append(act)

min_v = 1e5
for i in arr:
    min_v = min(i , min_v)

fig = sns.distplot(arr, norm_hist=True)

y_vals = fig.get_yticks()

fig.set_yticklabels(['{:3.0f}%'.format(x * 100 * (24369-23169)) for x in y_vals])

plt.xlabel("Frecuencia de corte (Hz)")
plt.ylabel("Casos")

plt.savefig("histogramas/output/histograma_marce.png")

plt.show()
