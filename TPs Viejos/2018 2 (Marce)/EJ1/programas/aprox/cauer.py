# coding=utf-8
import aprox
from math import sin, sinh, cos, cosh, pi,floor
from numpy import arcsinh, arccos, arccosh
import sympy as sp
import scipy as sci
from decimal import *

class Cauer(aprox.Aprox):
    #Al igual que con butter escribimos las tres funciones propias de la aproximación

    def __init__(self,plantilla):
        super(Cauer, self).__init__(plantilla)

    def getPoles(self, n_value, xi):
        [z, p, k] = sci.signal.ellipap(n_value,self.plantilla.data["ap"],self.plantilla.data["aa"])
        poles = []
        if n_value == 1:
            poles.append({"symbol": sp.symbols("p" + str(k)), "value": p})
        else:
            for k in range(0,len(p)):
                poles.append({"symbol": sp.symbols("p"+str(k)), "value": p[k]})
        return poles

    def getZeroes(self, n_value, xi):
        [z, p, k] = sci.signal.ellipap(n_value, self.plantilla.data["ap"], self.plantilla.data["aa"])

        zeroes = []

        for k in range(0, len(z)):
            zeroes.append({"symbol": sp.symbols("z" + str(k)), "value": z[k]})
        return zeroes

    def getZeroGain(self, n_value):
        [z, p, k] = sci.signal.ellipap(n_value, self.plantilla.data["ap"], self.plantilla.data["aa"])

        if n_value == 1:
            return 1
        else:
            return 10**(-self.plantilla.data["ap"]/20)
