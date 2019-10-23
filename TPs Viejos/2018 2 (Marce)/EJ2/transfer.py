# coding=utf-8

# coding=utf-8
import sympy as sp
from utils import algebra
from scipy import signal

s = sp.symbols("s")
R1 = 2.28e3
K = 0.162
C = 680e-12
a = 0.033
R2 = 20.5e3


H1 = (1/(1-K))*(a*s/(C*R1))/((s**2) + s*(2/(C*R2))*(1-(R2*K/(2*R1*(1-K)))) + (1/((C**2)*R1*R2)))

R1 = 1.39e3
K = 0.165
C = 1e-9
a = 0.033
R2 = 12.6e3

H2 = (1/(1-K))*(a*s/(C*R1))/((s**2) + s*(2/(C*R2))*(1-(R2*K/(2*R1*(1-K)))) + (1/((C**2)*R1*R2)))


H = H1*H2

#print(coef)

K = 0.162
C = 470e-12
R2 = 29.7e3

Zin = 100000/(1 - H1*(((1-K)/(s*C*R2)) + K))

tf = algebra.conseguir_tf(H, s)

tfZin = algebra.conseguir_tf(Zin, s)
