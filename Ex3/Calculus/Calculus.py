from scipy import signal
import pprint

class Sedra:
    def __init__(self,Wpol,Avol,Gb,C, name):
        self.WpoloDominante = Wpol
        self.Avol = Avol
        self.Gb = Gb
        self.C = C
        self.name = name
        return

    def resolve(self,tf):
        self.calcQandWo(tf)
        self.calcK()
        self.calcKminusculaAndMandNandG4()
        self.calcWpAndQp()
        self.calcGandCValues()
    
    def getValues(self):
        return self.values

    def calcQandWo(self,transferFunction):
        self.tf = transferFunction
        tf = self.tf
        self.num = [tf[0], tf[1], tf[2]]
        num = self.num
        self.den = [tf[3],tf[4], tf[5]]
        den = self.den
        self.wo = (den[0]/den[2])**-0.5
        self.Q = den[2]/(self.wo*den[1])
        return

    def calcK(self):
        if self.Q <1:
            self.Qo = self.Q/5
        else:
            self.Qo = self.Q/3
        self.K = (1/(2*self.Qo**2) * (1-self.Qo/self.Q) )+1
        return

    def calcKminusculaAndMandNandG4(self):
        self.Wz = (self.tf[2]/self.tf[0])**0.5
        self.n2 = self.tf[0]
        self.k = (self.n2*(self.Wz/self.wo)**2)/(1-self.Qo/self.Q)
        self.M = self.k*((self.K-1)/self.K) * (1+2*self.Qo**2 * (self.wo/self.Wz)**2) 
        self.N = self.k * (1-self.Qo/(self.K*self.Q))
        self.G4 = self.C * self.wo/(2*self.Qo)
        return

    def calcWpAndQp(self):
        self.wt = self.Avol * self.WpoloDominante
        self.wp = self.wo * (1+self.Qo*(self.wo/self.wt))
        temp = (1-(2*self.Qo*self.Q*(self.wo/self.wt)* (1/(2*self.Q) -self.wo/self.wt)) )
        self.Qp = self.Q * temp
        return

    def calcGandCValues(self):
        temp = {}
        temp['Ga'] = (self.K-1)*self.Gb
        Ga = temp['Ga']
        temp['Ga1'] = (1-self.k)* Ga
        temp['Ga2'] = self.k*Ga
        temp['G41'] = (1-self.N)*self.G4
        temp['G42'] = self.N*self.G4
        temp['C21'] = (1-self.M)*C
        temp['C22'] = self.M * C
        temp['Ra1'] = 1/temp['Ga1']
        temp['Ra'] = 1/temp['Ga']
        temp['Ra2'] = 1/temp['Ga2']
        temp['R41'] = 1/temp['G41']
        temp['R42'] = 1/temp['G42']
        self.values = temp
        return

    def printComponentValues(self):
        print('VALORES DE '+ self.name)
        pprint.pprint(self.values)
        return

    def setFilterValues(self):
        temp = {}
        temp['Q'] = self.Q
        temp['Qo'] = self.Qo
        temp['Wo'] = self.wo
        self.filterValues = temp
        return
    
    def printFilterValues(self):
        self.setFilterValues()
        print('VALORES DEL FILTRO '+self.name)
        pprint.pprint(self.filterValues)

##Usamos por ahora TL082

wpolodominante = 10
Avol = 100e3
wn = 2*3.1415 * 24.4E3
Gb = 1e-3
C = 10e-9

z,p,k = signal.ellip(4, 2, 40, wn, 'highpass', analog=True ,output='zpk')
hola = signal.zpk2sos(z, p, k)
tf1 = hola[0]
tf2 = hola[1]

Etapa1 = Sedra(wpolodominante,Avol,Gb,C,'ETAPA 1')
Etapa1.resolve(tf1)
Etapa2 = Sedra(wpolodominante,Avol,Gb,C,'ETAPA 2')
Etapa2.resolve(tf2)

Etapa1.printFilterValues()
Etapa1.printComponentValues()

Etapa2.printFilterValues()
Etapa2.printComponentValues()