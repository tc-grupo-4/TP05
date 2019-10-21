# coding=utf-8
import aprox
import sympy as sp
from utils import algebra
from decimal import *
from scipy import signal
import config
from numpy import sqrt



class Gauss(aprox.Aprox):
    def __init__(self, plantilla):
        super(Gauss, self).__init__(plantilla)
        self.factor = Decimal(self.plantilla.t0)

    def calcularDadoGamma(self, n_value, k=1, norm=-1, gamma=1):
        sn, s = sp.symbols("sn s")

        #print(num)
        den = 0
        fact = 1
        cnt = -1

        for i in range(1, n_value+1):
            fact *= i
            den += (gamma**i)*((s/sp.I)**(2*i)) / fact
        #print(den)

        exp = 1 / (1+den)
        #exp = self.plantilla.denormalizarFrecuencias(exp, s, sn)
        #print(exp)

        roots = algebra.getRoots(exp, s)
        roots[1] = algebra.filterRealNegativeRoots(roots[1])

        poles = []
        for i in roots[1]:
            poles.append({"value": i})

        exp = algebra.armarPolinomino(poles, [], s, 1)
        self.tf = algebra.conseguir_tf(exp, s, [])

        return self.tf

    def calcular(self, n_value, norm):
        self.calcularDadoGamma(n_value, 1, 0, 1)
        gd = self.evaluarRetardoDeGrupo(1e-3, 1e-6)
        gamma = (self.plantilla.t0 / gd) ** 2
        return self.calcularDadoGamma(n_value, 1, 0, gamma)

        # print("gamma = ", gamma, "gd = ", self.evaluarRetardoDeGrupo(1e-3, 1e-6))
    def computarGamma(self, n):
        self.calcularDadoGamma(n, 1, 0, 1)

        gd = self.evaluarRetardoDeGrupo(1e-3, 1e-6)

        gamma = (self.plantilla.t0 / gd) ** 2

        self.calcularDadoGamma(n, 1, 0, gamma)

        gain_nuevo = self.evaluarRetardoDeGrupo(1e-3, 1e-6)

        return 0


    def getMinNValue(self):
        for i in range(1, config.max_n):
            self.calcular(i, 0)

            gd = self.evaluarRetardoDeGrupo(self.plantilla.fp,self.plantilla.fp / (10**3) )

            if gd > self.plantilla.tmin:
                return i
        return -1