# coding=utf-8

from aprox.butter import Butter
from aprox.cheby import Cheby
from aprox.chebyinv import ChebyInv
from aprox.cauer import Cauer
from aprox.legendre import Legendre
from aprox.bessel import Bessel
from aprox.gauss import Gauss

mag_aprox = \
    {"Butterworth": Butter,
    "Chebycheff": Cheby,
    "Chebycheff inverso": ChebyInv,
    "Cauer": Cauer,
    "Legendre": Legendre}

pha_aprox = {
    "Bessel": Bessel,
    "Gauss": Gauss
}
