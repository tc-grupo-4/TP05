# coding=utf-8

from aprox import Aprox
from numpy.polynomial import legendre
from math import sqrt
import sympy as sp
from utils import algebra
from numpy import polynomial as P
import config
from scipy import signal


def get_a(i, n):
    if n % 2 == 0:
        k = int((n-2)/2)
        if (k + i) % 2 == 0:
            return 2 * i + 1
        else:
            return 0
    else:
        return 2*i+1


class Legendre(Aprox):
    def __init__(self, plantilla):
        super(Legendre, self).__init__(plantilla)

    def calcular(self, n, norm = False, k_factor = 1):
        # Atencion: Norm = calcular normalizada

        if n % 2 == 1:
            k = int((n-1)/2)
            arr = []
            for i in range(k+1):
                arr.append(get_a(i, n))

            poly = legendre.leg2poly(legendre.legint(legendre.legmul(arr, arr)))
        else:
            k = int((n-2)/2)
            arr = []
            for i in range(k+1):
                arr.append(get_a(i, n))

            leg_b = legendre.legmul(legendre.legmul(arr, arr), legendre.poly2leg([1, 1]))

            poly = legendre.leg2poly(legendre.legint(leg_b))

        exp = 0
        wn, sn, s, sa = sp.symbols("wn sn sa s")

        for i in range(len(poly)):
            exp += poly[i] * ((2*(wn**2)-1) ** i)
            exp -= poly[i] * ((-1)**i)

        if n % 2 == 1:
            exp = exp * 1 / (2 * (k+1)**2)
        else:
            exp = exp * 1 / ((k+1)*(k+2))

        exp = 1 / (1+self.getXi(0,n)**2*exp)
        exp = exp.subs(wn, sn/1j)

        roots = algebra.getRoots(exp, sn)
        roots[1] = algebra.filterRealNegativeRoots(roots[1])

        poles = []
        for i in roots[1]:
            poles.append({"value": i})

        exp = algebra.armarPolinomino(poles, [], sn, 1)
        self.tf_normalized = algebra.conseguir_tf(exp, sn, poles)

        if not norm:
            exp = self.plantilla.denormalizarFrecuencias(exp, sa, sn)
            self.getGainPoints()

            factor = (self.k1 - self.k2) * norm / 100 + self.k2

            exp = self.plantilla.denormalizarAmplitud(exp, s, sa, factor)

            self.tf = algebra.conseguir_tf(exp, s, [])

            return self.tf
        else:
            return self.tf_normalized

    def getMinNValue(self):
        for i in range(1, config.max_n):
            self.calcular(i)

            w, mag, pha = signal.bode(self.tf_normalized, [self.plantilla.wan])

            value = -mag[0]
            print("value = ", value)

            if value > self.plantilla.aa:
                return i

        return -1



