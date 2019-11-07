# coding=utf-8
from math import sqrt
from scipy import signal
import seaborn as sns
import matplotlib.pyplot as plt
from random import randrange
from math import pi
import numpy as np
from math import atan2
from make_histogram import make_histogram
from distutils.spawn import find_executable

f_range = np.logspace(4.3, 4.8, 10000)
w_range = [2 * pi * i for i in f_range]


res_tol = 1
cap_tol = 1
muestras =1800


k = 1e3
n = 1e-9

RA1 = [68, 12*k]
RA2 = [3*k, 15*k]
RB = [1*k, 1000]
R41 = [270, 6.2*k]
R42 = [12*k, 12*k]
R1 = [2400, 430]
C3 = [4.7*n, 4.7*n]
C21 = [4.7*n, 0.39*n]
C22 = [0.39*n, 4.7*n]


def disp(value, tol):
    min_value = value - value * tol / 100.0
    max_value = value + value * tol / 100.0

    rand = randrange(0, 1000)

    return min_value + (max_value - min_value) * rand / 1000.0


def conseguir_tf(ra1, ra2, r41, r42, r1, rb, c3, c21, c22):
    ga1 = 1.0/ra1
    ga2 = 1.0/ra2
    gb = 1.0/rb
    g42 = 1.0/r42
    g41 = 1.0/r41
    g1 = 1.0/r1

    n2 = (ga1 + ga2 + gb)/gb * c22 / (c21 + c22) - ga2/gb

    n1 = (ga1 + ga2 + gb) / gb * g42 * (1/(c21 + c22) + 1/c3) - ga2 / gb * (g1 / (c21 + c22) + (g41 + g42)*(1/(c21 + c22) + 1/c3))

    n0 = g1 * (g41 + g42) / (c3 * (c21 + c22)) * (g42 / (g41 + g42) * (ga1 + ga2 + gb)/gb - ga2/gb)

    w02 = g1*(g41+g42) / (c3 * (c21 + c22))

    b = (g41 + g42) * (1/(c21+c22) + 1/c3) - (g1 / (c21 + c22)*(ga1+ga2)/gb)
    #print([n2, n1, n0], [1, b, w02])
    return signal.lti([n2, n1, n0], [1, b, w02])


sns.set(style="darkgrid")

#tips = sns.load_dataset("tips")
#tips = {"im":[2,5],"re":[3,5]}
# g = sns.jointplot("total_bill", "tip", data=tips, kind="reg"
#                   xlim=(0, 60), ylim=(0, 12), color="m", height=7)
#




def plot_hist(circuit_id, mode, sing_id, width, width2):
    data = {"w0": [], "q": []}
    
    sns.set_style("whitegrid")
    for i in range(muestras):
        tf = conseguir_tf(
            ra1=disp(RA1[circuit_id], res_tol),
            ra2=disp(RA2[circuit_id], res_tol),
            r41=disp(R41[circuit_id], res_tol),
            r42=disp(R42[circuit_id], res_tol),
            r1=disp(R1[circuit_id], res_tol),
            rb=disp(RB[circuit_id], res_tol),
            c3=disp(C3[circuit_id], cap_tol),
            c21=disp(C21[circuit_id], cap_tol),
            c22=disp(C22[circuit_id], cap_tol)
        )

        if mode == "poles":
            info = tf.poles[sing_id]
        else:
            info = tf.zeros[sing_id]
        w0 = sqrt(info.real**2 + info.imag ** 2)
        data["w0"].append(2*pi*w0)
        data["q"].append(- w0 / (2 * info.real))

    # g = sns.jointplot("w0", "q", data=data, kind="reg",
    #                   color="m", height=7)

    # plt.xlabel("Fo (Hz)")
    #
    # plt.ylabel("Q")
    if str(mode) == "poles":
        textmode = "Polo"
    else:
        textmode = "Cero"
    plt.title(textmode + " " + str(sing_id+1) + ", etapa "+str(circuit_id+1))
    
    make_histogram(variable="Fo",
                   unidad="Hz",
                   data=data["w0"],
                   filename="histograma_w0_"+str(mode)+"_"+str(sing_id) + str(circuit_id) +".png",
                   bar_width=width)

    plt.title(textmode + " " + str(sing_id+1) + ", etapa "+str(circuit_id+1))
    
    make_histogram(variable="Q",
                   unidad="adimensional",
                   data=data["q"],
                   filename="histograma_q_" + str(mode) + "_" + str(sing_id) + str(circuit_id) + ".png",
                   bar_width=width2)


plot_hist(circuit_id=0,
          mode="poles",
          sing_id=0,
          width = (212850-212550)*2*pi,
          width2= 0.780689-0.776144)

plot_hist(circuit_id=0,
          mode="poles",
          sing_id=1,
          width = (213850-213550)*2*pi,
          width2 = 0.777032-0.772392)

plot_hist(circuit_id=1,
          mode="poles",
          sing_id=0,
          width=(128375-128200)*2*pi,
          width2=4.090-4.076)

plot_hist(circuit_id=1,
          mode="poles",
          sing_id=1,
          width=(128110-127924)*2*pi,
          width2=4.08722-4.07296)


plot_hist(circuit_id=0,
          mode="zeros",
          sing_id=0,
          width = 197323-195723,
          width2= 0)

plot_hist(circuit_id=0,
          mode="zeros",
          sing_id=1,
          width = 196800-195223,
          width2 = 0.777032-0.772392)

plot_hist(circuit_id=1,
          mode="zeros",
          sing_id=0,
          width=446831-446125,
          width2=4.090-4.076)

plot_hist(circuit_id=1,
          mode="zeros",
          sing_id=1,
          width=446161-445415,
          width2=4.08722-4.07296)
