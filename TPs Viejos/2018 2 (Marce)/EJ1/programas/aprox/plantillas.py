from math import pi, sqrt
import config
from numpy import logspace, log10
from decimal import *

# Esta plantilla sirve para filtros que tengan restricciones sobre la atenuacion
# Cumple la funcion de recopilar los datos, y colocarlos de manera comoda para su uso
# Tambien se encarga de las sustituciones algebraicas para las denormalizaciones,
# que son comunes a todas las aproximaciones de magnitud

# Nomenclatura
# "pb": pasa bajos
# "pa": pasa altos
# "bp": pasa banda
# "br": rechaza banda

EPS = 1e-10


class Plantilla:
    aa, ap, b, w0, f0 = None, None, None, None, None
    fa, fp, fa0, fa1, fp0, fp1 = None, None, None, None, None, None
    deltaFa, deltaFp = None, None
    denorm, corrupta, type = None, None, None
    t0, tmin, type = None, None, None

    def __init__(self, data):

        self.data = data

        if config.debug:
            print("Inicializando plantilla con data = ", data)

        if data["type"] == "pb":
            self.type = "magnitud"
            self.corrupta = self.validar1erOrden(data)
            self.wan = data["fa"] / data["fp"]
            self.calcularDatos1erOrden(data)

        elif data["type"] == "pa":
            self.type = "magnitud"
            self.corrupta = self.validar1erOrden(data)
            self.wan = data["fp"] / data["fa"]
            self.calcularDatos1erOrden(data)

        elif data["type"] == "bp":
            self.type = "magnitud"
            self.corrupta = self.validar2doOrden(data)

            self.ap = data["ap"]
            self.aa = data["aa"]

            self.calcularDatos2doOrden(data)
            self.ajustarAsimetria()

            self.wan = self.deltaFa / self.deltaFp

        elif data["type"] == "br":
            self.type = "magnitud"
            self.corrupta = self.validar2doOrden(data)

            self.ap = data["ap"]
            self.aa = data["aa"]

            self.calcularDatos2doOrden(data)
            self.ajustarAsimetria()

            self.wan = self.deltaFp / self.deltaFa
        elif data["type"] == "gd":
            self.type = "fase"

            self.corrupta = self.validarFase(data)

            self.t0 = data["t0"]/1000.0
            self.tmin = data["tmin"]/1000.0
            self.fp = data["fp"]

        else:
            print("Plantilla  llamada erroneamente")

    def ajustarAsimetria(self):
        # Se ajusta en caso de que el filtro pasabanda o rechaza banda no cumpla
        # simetria geometrica


        if self.data["type"] == "bp":
            letter = "a"
        else:
            letter = "p"


        fa_mas = self.f0**2 / self.data["f"+letter+"-"]
        fa_menos = self.f0**2 / self.data["f"+letter+"+"]
        #print("fa- = ",fa_menos)
        if fa_mas < self.data["f"+letter+"+"]:
            self.data["f"+letter+"+"] = fa_mas
            if letter == "a":
                self.fa1 = fa_mas
            else:
                self.fp1 = fa_mas
        else:
            self.data["f"+letter+"-"] = fa_menos
            if letter == "a":
                self.fa0 = fa_menos
            else:
                self.fp0 = fa_menos


        self.deltaFp = self.fp1-self.fp0
        self.deltaFa = self.fa1 - self.fa0


        self.b = self.deltaFp / self.f0
        self.q = self.f0 / self.deltaFp

        print(self.fp0 , self.fa0, self.fa1, self.fp1)

    def validar1erOrden(self, data):
        if data["fp"] < 0:
            return 1
        if data["fa"] < 0:
            return 1
        if data["ap"] - EPS > data["aa"]:
            return 1
        if data["type"] == "pb" and data["fp"] - EPS > data["fa"]:
            return 1
        if data["type"] == "pa" and data["fa"] - EPS > data["fp"]:
            return 1
        return 0

    def validar2doOrden(self, data):
        if data["fa-"] < 0:
            return 1
        if data["fp-"] < 0:
            return 1
        if data["fp+"] < 0:
            return 1
        if data["fa+"] < 0:
            return 1
        if data["type"] == "bp":
            if not (data["fa-"] < data["fp-"] < data["fp+"] < data["fa+"]):
                return 1
        else:
            if not (data["fp-"] < data["fa-"] < data["fa+"] < data["fp+"]):
                return 1
        return 0

    def validarFase(self, data):
        if data["tmin"] - EPS > data["t0"]:
            return 1
        if data["t0"] < 0:
            return 1
        if data["tmin"] < 0:
            return 1

    def calcularDatos1erOrden(self, data):
        self.wpn = 1
        self.ap = data["ap"]
        self.aa = data["aa"]

        self.fa = data["fa"]
        self.fp = data["fp"]
        self.wa = data["fa"] * 2 * pi
        self.wp = data["fp"] * 2 * pi

    def calcularDatos2doOrden(self, data):

        self.deltaFa = data["fa+"] - data["fa-"]
        self.deltaFp = data["fp+"] - data["fp-"]
        if self.data["type"] == "bp":
            self.f0 = sqrt(data["fp+"] * data["fp-"])
        else:
            self.f0 = sqrt(data["fa+"] * data["fa-"])

        self.w0 = self.f0 * 2 * pi
        #self.b = self.deltaFp / self.f0
        #self.q = self.f0 / self.deltaFp
        if data["type"] == "pb":
            self.wan = self.deltaFa / self.deltaFp
        elif data["type"] == "pa":
            self.wan = self.deltaFp / self.deltaFa

        self.fa0 = data["fa-"]
        self.fa1 = data["fa+"]
        self.fp0 = data["fp-"]
        self.fp1 = data["fp+"]

    def denormalizarFrecuencias(self, exp, s, sn):
        # se inserta un polinomio normalizado expresado en la variable s y se aplica la
        # sustitucion necesaria para la plantilla para la denormalizacion por frecuencaias
        # var: variable simbolica (s)
        return exp.subs(sn, self.getSubExpression(s))

    def denormalizarAmplitud(self, exp, s, sn, k):
        # Update: NO se usa mas, la amplitud se ajusta con la influencia de xi sobre los polos transferencia
        # A transferencia

        # se inserta un polinomino normalizado con ganancia 3db en wp en la variable s y se aplica la denormalizacion
        # de amplitud para tener la ganancia correcta en wp
        # Es necesario insertar el valor de Tn en wan, el cual depende de la aproximacion usada


        return exp.subs(sn, s * k)

    def denormalizar0_100(self, norm): # buscamos la conversion s -> sk tal que se cumpla H(wp)=Ap o H(wa)=Aa
        pass

    def getSubExpression(self, s):
        # Conseguimos la expresion correspondiente de sustitución segun el tipo de filtro
        if self.data["type"] == "pb":
            return s / self.wp
        elif self.data["type"] == "pa":
            return self.wp / s
        elif self.data["type"] == "bp":
            return (s / Decimal(self.w0) + Decimal(self.w0) / s) * Decimal(self.q)
        elif self.data["type"] == "br":
            return Decimal(self.b) / (s / Decimal(self.w0) + Decimal(self.w0) / s)
        elif self.data["type"] == "gd":
            return s * Decimal(self.t0)

    def getSubExpressionAmplitude(self, s, n, tn_wan, denorm):
        # Consguiemos el rango de xi que ajustan la amplitud de manera correcta
        # Actualmente no esta en uso pero proximamente deberá ser empezada a usar

        xi_1 = sqrt((10 ** (self.data["ap"] / 10)) - 1)
        xi_2 = sqrt(((10 ** (self.data["aa"] / 10)) - 1)/tn_wan**2)

        factor_1 = xi_1 ** (1/n)
        factor_2 = xi_2 ** (1/n)

        max_factor = max(factor_1, factor_2)
        min_factor = min(factor_1, factor_2)

        factor = (max_factor - min_factor) * (denorm / 100.0) + min_factor

        return s * factor

    def getPlantillaPoints(self, min_freq, max_freq, min_amp, max_amp):
        # Obtener las coordenadas para dibujar la plantilla, este codigo es muy tedioso ya que
        # se debe colocar todas las coordenadas de ls lineas de la plantilla

        x_points = x_points_b = x_points_c = []
        y_points = y_points_b = y_points_c = []

        if self.data["type"] == "pb":
            min_freq = min(min_freq, self.fp)
            max_freq = max(max_freq, self.fa) # Ajuste para que graficamente si la escala es mala se vea mejor

            x_points = [min_freq, self.fp, self.fp]
            y_points = [self.ap, self.ap, max_amp]

            x_points_b = [self.fa, self.fa, max_freq]
            y_points_b = [min_amp, self.aa, self.aa]

        elif self.data["type"] == "pa":
            min_freq = min(min_freq, self.fa)
            max_freq = max(max_freq, self.fp)

            #print(self.fa,self.fp)
            #print(min_freq, max_freq)

            x_points = [min_freq, self.fa, self.fa]
            y_points = [self.aa, self.aa, min_amp]

            x_points_b = [self.fp, self.fp, max_freq]
            y_points_b = [max_amp, self.ap, self.ap]

        elif self.data["type"] == "bp":
            x_points = [min_freq, self.fa0, self.fa0]
            y_points = [self.aa, self.aa, min_freq]

            x_points_c = [self.fa1, self.fa1, max_freq]
            y_points_c = [min_amp, self.aa, self.aa]

            x_points_b = [self.fp0, self.fp0, self.fp1, self.fp1]
            y_points_b = [max_amp, self.ap, self.ap, max_amp]

        elif self.data["type"] == "br":
            x_points = [min_freq, self.fp0, self.fp0]
            y_points = [self.ap, self.ap, max_amp]

            x_points_c = [self.fp1, self.fp1, max_freq]
            y_points_c = [max_amp, self.ap, self.ap]
            #print(self.fa0)
            x_points_b = [self.fa0, self.fa0, self.fa1, self.fa1]
            y_points_b = [min_amp, self.aa, self.aa, min_amp]
        elif self.data["type"] == "gd":
            x_points = [min_freq, self.fp, self.fp]
            y_points = [self.tmin*1000, self.tmin*1000, min_amp]

        data1 = dict()
        data1["A"] = x_points, y_points
        data1["B"] = x_points_b, y_points_b
        data1["C"] = x_points_c, y_points_c

        return data1

    def getDefaultFreqRange(self):
        # Conseguimos escala defecto para que se vea bien el grafico
        if self.data["type"] == "pa":
            return logspace(log10(self.data["fa"])-1.5, log10(self.data["fa"])+1.5, 10000)
        elif self.data["type"] == "pb":
            return logspace(log10(self.data["fp"]) - 1.5, log10(self.data["fp"]) + 1.5, 10000)
        elif self.data["type"] == "bp":
            return logspace(log10(self.data["fa-"]) - 1.5, log10(self.data["fa+"]) + 1.5, 10000)
        elif self.data["type"] == "br":
            return logspace(log10(self.data["fp-"]) - 1.5, log10(self.data["fp+"]) + 1.5, 10000)
        elif self.data["type"] == "gd":
            return logspace(log10(self.data["fp"]) - 1.5, log10(self.data["fp"]) + 1.5, 10000)

    def getTinyFreqRange(self):
        # Conseguimos escala defecto para que se vea bien el grafico
        if self.data["type"] == "pa":
            return logspace(log10(self.data["fa"])-0.5, log10(self.data["fp"])+0.5, 10000)
        elif self.data["type"] == "pb":
            return logspace(log10(self.data["fp"]) - 0.5, log10(self.data["fa"]) + 0.5, 10000)
        elif self.data["type"] == "bp":
            return logspace(log10(self.data["fa-"]) - 0.5, log10(self.data["fa+"]) + 0.5, 10000)
        elif self.data["type"] == "br":
            return logspace(log10(self.data["fp-"]) - 0.5, log10(self.data["fp+"]) + 0.5, 10000)
        elif self.data["type"] == "gd":
            return logspace(log10(self.data["fp"]) - 0.5, log10(self.data["fp"]) + 0.5, 10000)