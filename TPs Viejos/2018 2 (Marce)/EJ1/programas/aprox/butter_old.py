
# Codigo viejo para calcular butter
# Fuera de uso


from scipy import signal
import matplotlib.pyplot as plt
from numpy import *
import cmath
from numpy.polynomial import polynomial as P
from numpy import *
from scipy import signal



from control import *
from aprox import *
import control as ctrl
from control import matlab
import sympy as sp
import utils.algebra as algebra
import config


### Nomenclatura
# hp: high pass
# lp: low pass
# bp: band pass
# br: band reject


sn, s = sp.symbols("sn s")


class Butter(Aprox):
    def __init__(self):
        self.f = None
        self.mag = None
        self.phase = None
        self.fp= None
        self.fs= None
        self.Ap=None
        self.As=None
        self.n=None
        self.poles = None
        self.symbolic_poles = None
        self.transferFunction = None

    def configure(self, data):
        self.filterData = data
        self.filterType = data["filterType"]
        self.Ap = data["ap"]
        self.As = data["as"]
        self.computarN()

    def getWaN(self):
        if self.filterType == "lp":
            return self.filterData["fp"] / self.filterData["fa"]
        elif self.filterType == "hp":
            return self.filterData["fa"] / self.filterData["fp"]
        elif self.filterType == "bp":
            deltaFa = self.filterData["fa+"]-self.filterData["fa-"]
            deltaFp = self.filterData["fp+"]-self.filterData["fp-"]
            return deltaFa / deltaFp
        elif self.filterType == "br":
            deltaFa = self.filterData["fa+"] - self.filterData["fa-"]
            deltaFp = self.filterData["fp+"] - self.filterData["fp-"]
            return deltaFp / deltaFa

    def areValidInputs(self, optionSelected):
        if optionSelected == "Con N":
            if self.n < 0:
                return 0
            if abs(self.n-int(self.n)) < EPS: #checkeo que sea entero
                return 0
        elif optionSelected == "Sin N":
            if self.fp > self.fs:
                return 0
            if self.fp < 0 or self.fs < 0:
                return 0
        return 1

    def computarN(self):

        self.xi = sqrt((10 ** (self.Ap / 10)) - 1)

        num = log10(sqrt((10**(self.As/10))-1) / self.xi)
        den = log10(self.getWaN())
        self.n = math.ceil(num/den)
        if config.debug:
            print("xi=", self.xi)
            print("n = ", self.n)

    def setN(self, n):
        self.n = n

    def getBodeData(self, points):
        self.getNormalizedPoles(self.n)
        if self.filterType == "lp":
            self.transferFunction = self.denormalizar(s/(self.filterData["fp"] * 2 * pi))
        elif self.filterType == "hp":
            self.transferFunction = self.denormalizar((self.filterData["fp"] * 2 * pi)/s)
        elif self.filterType == "bp":
            f0 = sqrt(self.filterData["fp+"]*self.filterData["fp-"])
            w0 = 2*pi*f0
            b = (self.filterData["fp+"]-self.filterData["fp-"]) / f0
            self.transferFunction = self.denormalizar(1/b*(s/w0+w0/s))
        elif self.filterType == "br":
            f0 = sqrt(self.filterData["fp+"] * self.filterData["fp-"])
            w0 = 2 * pi * f0
            b = (self.filterData["fp+"] - self.filterData["fp-"]) / f0
            self.transferFunction = self.denormalizar(1/(1/b*(s/w0+w0/s)))

        w, mag, phase = signal.bode(self.transferFunction, points)
        self.f = w/(2*pi)
        self.mag = mag
        self.phase = phase

    def getNormalizedPoles(self,n):
        self.poles = []
        for k in range(1, n + 1):
            self.poles.append(1/(self.xi ** (1 / self.n))*(cmath.exp(1j * (2 * k + n - 1) * (pi / (2 * n)))))

    def denormalizar(self, substituteExpression):
        h = 1
        for pl in self.poles:
            h = h * 1 / ((sn - pl) / (-pl))

        h = h.subs(sn, substituteExpression)

        value = algebra.expand_and_get_coef(h, s)
        transferFunction = signal.lti(value[0], value[1])

        return transferFunction

    def gather1stand2ndOrder(self):
        newPoles = []
        for i in range(len(self.poles)):
            if self.poles[i].imag >= 0:
                newPoles.append(self.poles[i])
        return newPoles

    def LP_FreqTransform2ndOrd(self,sk, wp):  # esta funcion necesita un solo conjugado!!
        num = [1]
        den = [1 / wp ** 2, -2 * sk.real / wp, abs(sk) ** 2]
        return num, den

    def LP_FreqTransform1stdOrd(self,sk, wp):
        num = [wp]
        den = [1, -sk * wp]
        return num, den

    def computar(self, freqRange,optionSelected, points = []):
        if self.areValidInputs(optionSelected):
            if optionSelected == "sin N":
                self.computarN()
            self.getBodeData(points)
