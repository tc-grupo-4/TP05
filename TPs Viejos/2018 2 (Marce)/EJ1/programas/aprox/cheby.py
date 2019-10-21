# coding=utf-8
import aprox
from math import sin, sinh, cos, cosh, pi, sqrt, ceil
from numpy import arcsinh, arccos, arccosh
import sympy as sp
from decimal import *

class Cheby(aprox.Aprox):
    #Al igual que con butter escribimos las tres funciones propias de la aproximación

    def __init__(self,plantilla):
        super(Cheby, self).__init__(plantilla)

    def getPoles(self, n_value, xi):
        poles = []

        for k in range(1, n_value+1):
            alpha_k = (2*k-1)/(2*n_value) * pi
            beta = -1/n_value * arcsinh(1/xi)

            re = Decimal(sin(alpha_k) * sinh(beta))
            im = Decimal(cos(alpha_k) * cosh(beta))

            poles.append({"symbol": sp.symbols("p"+str(k)), "value": re + im * sp.I})

        return poles

    def getZeroes(self, n_value, xi):
        return []

    def Tn(self, n, w):
        if w < 1:
            return cos(n*arccos(w))
        else:
            return cosh(n*arccosh(w))

    def getZeroGain(self, n_value):
        if n_value % 2 == 0:
            return 10**(-self.plantilla.data["ap"]/20.0)
        else:
            return 1
    def getMinNValue(self):
        xi = sqrt((10**(self.plantilla.ap/10))-1)
        return ceil(arccosh(sqrt(10**(self.plantilla.aa/10.0)-1)/xi)/arccosh(self.plantilla.wan))