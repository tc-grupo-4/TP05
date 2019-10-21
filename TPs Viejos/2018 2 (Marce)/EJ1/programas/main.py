# coding=utf-8

from aprox import plantillas, bessel
from numpy import linspace
from utils import round_sig
import sympy as sp
from scipy import signal
from utils.algebra import factorizar_tf
from utils.etapas import getSing2OrderExpression
from utils import etapas
import matplotlib.pyplot as plt

fp = 2200
fa = 10400
ap = 3
tol = 0.95


for t0 in linspace(0.04, 0.2, 20):

    plantilla = plantillas.Plantilla(
        {"type": "gd",
         "t0": t0,
         "tmin": t0*0.95,
         "fp": fp}
    )

    b = bessel.Bessel(plantilla)

    min_n = -1

    for n_value in range(1, 20):
        b.calcular(n_value)
        mag, pha = b.evaluarAproximacion(fp)
        at = -mag

        gd = b.evaluarRetardoDeGrupo(fp, fp*0.001)
        if at < ap and gd > t0 * 0.001 * tol:
            min_n = n_value
            break
    text_file = open("output.txt", "w")

    print("-------------")
    if min_n == -1:
        print("gd = ", gd, " not found")
    else:
        print("t0 = ", t0, "n =", min_n)
        # Ahora checkeamos si cumple la condicion

        b.calcular(min_n)

        mag, pha = b.evaluarAproximacion(fa)
        at = -mag

        mag, pha = b.evaluarAproximacion(fp)
        at_fp = -mag

        gd = b.evaluarRetardoDeGrupo(fp, fp*0.001) * 1000

        if at > 40:
            print("Gd(fp) = ", round_sig(gd, 4), "ms At(fp) = ", round_sig(at_fp,4), " At(fa) = ", round_sig(at,4), " Cumple")
            print("H(s) = ", etapas.getFacto2orderExpression(b.tf))
            print("coef = ", b.coef)
        else:
            print("Gd(fp) = ", round_sig(gd, 4)," ms At(fp) = ", round_sig(at_fp,4), "At(fa) = ", round_sig(at,4))
            print("H(s) = ", etapas.getFacto2orderExpression(b.tf))
            print("coef = ", b.coef)


