from computar_maximos import conseguir_fp
from read_spice_montecarlo import read_file_spice
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import norm

#sns.set_style('darkgrid')

#np.random.seed(444)
#np.set_printoptions(precision=3)

#d = np.random.laplace(loc=15, scale=3, size=500)
#print(d)
# d = [4,3,5,2,10]
# sns.distplot(d, fit=stats.laplace, kde=False)
# plt.show()

#data = read_file_spice("EJ1/Circuito con Legendre/Simulacion/BodeMontecarlo.txt")


arr = [2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5.5, 5, 6]

# for i in range(len(data)):
#     act = conseguir_fp(data[i], -3)
#
#     arr.append(act)
#
# min_v = 1e5
# for i in arr:
#     min_v = min(i , min_v)

fig = sns.distplot(arr)

y_vals = fig.get_yticks()
#print(y_vals)
sum = 0
for i in y_vals:
    sum += i
# print(sum)
factor = 1/sum

fig.set_yticklabels(['{:3.0f}%'.format(x * factor * 100) for x in y_vals])


#plt.savefig("histograma_marce.png")
plt.show()