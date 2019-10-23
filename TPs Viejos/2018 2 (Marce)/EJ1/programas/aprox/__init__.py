from utils.algebra import armarPolinomino, conseguir_tf, expand_and_get_coef, conseguir_coef
from utils.etapas import getSing, DataEtapas
import sympy as sp
from scipy import signal
from math import pi, sqrt
from numpy import log10, logspace, linspace
import config
from control import evalfr

EPS = 1e-15

# En este modulo estarán programadas todas las aproximaciones





class Aprox:
    # Aproximacion padre, con todas las funciones generales de una aproximacion
    polynominal = None
    data = dict()
    tf = None
    tf_normalized = None
    etapas = None
    k1 , k2 = None, None
    loadingReference = None

    def __init__(self, plantilla):
        self.plantilla = plantilla

    def setLoadingReference(self, ref):
        self.loadingReference = ref

    def calcular(self, n_value, norm, k=1): # calcular mediante N la funcion transferencia de la aproximacion
        poles = self.getPoles(n_value, self.getXi(norm, n_value))
        zeroes = self.getZeroes(n_value, self.getXi(norm, n_value))
        sn, sa, s = sp.symbols("sn sa s")
        pol = armarPolinomino(poles, zeroes, sn, self.getZeroGain(n_value))
        self.tf_normalized = conseguir_tf(pol, sn, poles)
        self.getGainPoints()
        factor = (self.k1-self.k2)*norm/100 + self.k2

        pol = self.plantilla.denormalizarAmplitud(pol, sa, sn, factor)

        #pol = self.plantilla.denormalizarAmplitud(pol, sa, sn, n_value, 1, 0)
        pol = self.plantilla.denormalizarFrecuencias(pol, s, sa)
        #print(pol)

        self.tf = conseguir_tf(pol, s, poles)
        self.updateEtapas()
        return self.tf

    def getMinNValue(self):
        return -1

    def getQValues(self):
        if not self.etapas:
            return -1
        maxQ = 0
        for etapa in self.etapas.polos:
            maxQ = max(maxQ, etapa.q)
        for etapa in self.etapas.ceros:
            maxQ = max(maxQ, etapa.q)
        return maxQ

    def getPoles(self, n_value, xi):
        pass

    def getZeroes(self, n_value, xi):
        pass

    def getData(self, start_freq, end_freq):
        pass

    def getZeroGain(self, n_value):
        return 1

    # def getXi(self, norm, n):
    #     xi1 = self.getXiA(n)
    #     xi2 = self.getXiB(n)
    #     if xi1 > xi2:
    #         norm = 100 - norm
    #     if config.debug:
    #         print("Xi values:", xi1, xi2)
    #
    #     return (max(xi1, xi2) - min(xi1, xi2))*(norm**n)/(100**n) + min(xi1, xi2)

    def getXiA(self, n):
        return sqrt(10**(self.plantilla.data["ap"]/10.0)-1)

    def getXiB(self, n):
        # Atencion: debe ya haberse calculado la aproximacion alguna vez para que funcione esta funcion

        return sqrt(10**(self.plantilla.data["aa"]/10.0)-1) / self.Tn(n, self.plantilla.wan)

    def getXiData(self, norm, n):
        at = 10**(self.plantilla.data["ap"]/10.0) / self.getZeroGain(n)**2

        return at

    def getXi(self, norm , n):
        at = self.getXiData(norm, n)

        return sqrt(at-1)

    def updateEtapas(self):
        if config.debug:
            print("Actualizando etapas")
        if not self.tf:
            if config.debug:
                print("Ocurrio algo raro")
            return None

        poles = self.tf.poles
        zeros = self.tf.zeros

        self.etapas = DataEtapas(getSing(poles), getSing(zeros))

        return self.etapas

    def evaluarAproximacion(self, f):
        if self.tf:
            w, mag, pha = signal.bode(self.tf, [2*pi*f])
            return mag[0], pha[0]
        else:
            return -1

    def evaluarRetardoDeGrupo(self, f, df):
        if self.tf:
            w, mag, pha = signal.bode(self.tf, [2*pi*f, 2*pi*(f+df)])
            return - (pha[1] - pha[0]) / 180 * pi / (w[1] - w[0])
        else:
            return -1

    def getGainPoints(self):# Encontrar numericamente w1,w2 consecutivos tales que H(w1) = Ap, y w tal que H(w2) = Aa
        w, mag, pha = signal.bode(self.tf_normalized, logspace(-8, log10(self.plantilla.wan)+8, 10000))

        ap = self.plantilla.data["ap"]
        aa = self.plantilla.data["aa"]

        ap_point = -1
        aa_point = -1

        for i in range(len(mag)-1, -1, -1):
            #print(mag[i], w[i])
            if aa_point == -1 and mag[i] > (-aa)*0.95:
                j = i
                while mag[j] > -aa:
                    j += 1
                    aa_point = j

            if ap_point == -1 and mag[i] > (-ap):
                ap_point = i-1
                break

        self.k1 = w[aa_point] / self.plantilla.wan
        self.k2 = w[ap_point]

        #print("Puntos magicos: ")

        #print(mag[ap_point], mag[aa_point])
        #print(w[ap_point], w[aa_point])
