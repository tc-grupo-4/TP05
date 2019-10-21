import aprox
from math import pi, sqrt, ceil
from cmath import exp
import sympy as sp
from decimal import *
from numpy import log10


class Butter(aprox.Aprox):
    # Filtro butterworth, sobre-escribimos la funcion para obtener los polos, la funcion
    # para obtener Tn y la ganancia en w=0, que son propias de butter

    def __init__(self, plantilla):
        super(Butter, self).__init__(plantilla)

    def getPoles(self, n, xi):
        poles = []
        symbols = []

        mod = 1 / (xi ** (1 / float(n)))
        print("mod = ", mod)
        for k in range(1, n+1):

            pole = mod * exp(1j * (2 * k + n - 1) * (pi / (2 * n))) # Formula de polos
            re = Decimal(pole.real)
            im = Decimal(pole.imag)
            poles.append({"symbol": sp.symbols("p"+str(k)), "value": re + im * sp.I})

        return poles

    def getZeroes(self, n_value, xi):
        return []

    def Tn(self, n, w):
        return w ** n

    def getZeroGain(self, n_value):
        return 1

    def getMinNValue(self):
        xi= sqrt(10**(self.plantilla.data["ap"]/10)-1)
        return ceil(log10(sqrt(10**(self.plantilla.data["aa"]/10)-1)/xi)/log10(self.plantilla.wan))

    def getDenormConstant(self, norm):
        pass
