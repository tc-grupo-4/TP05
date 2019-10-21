# coding=utf-8

import aprox
import sympy as sp
from utils import algebra
import config
from decimal import *

from scipy import signal
from math import pi

polyBessel = dict()


def computeBesselPoly(n, var):

    if polyBessel.get(n):
        return polyBessel[n]

    # No lo calculamos ya, asi que debemos calcular el bessel N

    # casos base
    if n == 1:
        return var + 1
    if n == 2:
        return var ** 2 + 3 * var + 3

    # Caso n
    return sp.expand((2*n-1)*computeBesselPoly(n-1, var) + var * var * computeBesselPoly(n-2, var))


class Bessel(aprox.Aprox):
    def __init__(self, plantilla):
        super(Bessel, self).__init__(plantilla)
        self.factor = Decimal(self.plantilla.t0)

    def calcular(self, n_value, k=1, norm = -1):
        sn, s = sp.symbols("sn s")
        self.var = s

        num = computeBesselPoly(n_value, sn).evalf(subs={sn: 0})

        #print(num)
        den = computeBesselPoly(n_value, sn)
        #print(den)

        exp = num / den
        exp = self.plantilla.denormalizarFrecuencias(exp, s, sn)
        self.exp = exp
        self.coef = algebra.conseguir_coef(exp, s)

        self.tf = algebra.conseguir_tf(exp, s, [])
        return self.tf

    def getMinNValue(self):
        ans = 1
        found = 0
        for i in range(1, config.max_n+1):
            ans = i
            self.calcular(i, 1)

            gd = self.evaluarRetardoDeGrupo(self.plantilla.fp, self.plantilla.fp * 0.001)
            #print("gd = ",gd)
            if gd > self.plantilla.tmin:
                found = 1
                break
        if found:
            return ans
        else:
            return -1
