from scipy import signal
import pprint

class Sedra:
    def __init__(self,Wpol,Avol,Rb,C,tf, name):
        self.WpoloDominante = Wpol
        self.Avol = Avol
        self.Rb = Rb
        self.Gb = 1/Rb
        self.C = C
        self.name = name
        self.tf = tf
        self.resolve()
        return

    def resolve(self):
        self.calcQandWo()
        self.calcK()
        self.calcKminusculaAndMandNandG4()
        self.calcWpAndQp()
        self.calcGandCValues()
    
    def getValues(self):
        return self.values

    def calcQandWo(self):
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
        Ga = (self.K-1)*self.Gb
        Ga1 = (1-self.k)* Ga
        Ga2 = self.k*Ga
        G41 = (1-self.N)*self.G4
        G42 = self.N*self.G4
        temp['C21'] = (1-self.M)*self.C
        temp['C22'] = self.M * self.C
        temp['C3'] = self.C
        temp['Ra1'] = 1/Ga1
        #temp['Ra'] = 1/Ga
        temp['Ra2'] = 1/Ga2
        temp['R41'] = 1/G41
        temp['R42'] = 1/G42
        G1 = 2 * self.Qo * self.wp * (self.C * (temp['C21']+temp['C22']))**0.5
        temp['R1'] = 1 / G1
        temp['Rb'] = self.Rb
        self.values = temp
        return

    def printComponentValues(self):
        print('\nVALORES DE '+ self.name)
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


if __name__ == "__main__":
    ##Usamos por ahora TL082
    wpolodominante = 10
    Avol = 100e3
    wp = 2*3.1415 * 24.4E3
    ws = 2*3.1415 * 12.2e3
    Rb = 10e3
    C = 1e-9

    n,wn = signal.ellipord(wp,ws,2,40,analog=True)
    z,p,k = signal.ellip(n, 2, 40, wn, 'highpass', analog=True, output='zpk')
    TransferFunction = signal.zpk2sos(z, p, k)
    tf1 = TransferFunction[0]
    tf2 = TransferFunction[1]

    Etapa1 = Sedra(wpolodominante,Avol,Rb,C,tf1,'ETAPA 1')
    Etapa2 = Sedra(wpolodominante,Avol,Rb,C,tf2,'ETAPA 2')

    #Etapa1.printFilterValues()
    Etapa1.printComponentValues()

    #Etapa2.printFilterValues()
    Etapa2.printComponentValues()

    ## Solo para mi despues queda comentado
    num,den = signal.ellip(n, 2, 80, wn, 'highpass', analog=True)
    print('Numerador='+str(num[0])+','+str(num[1])+','+str(num[2])+','+str(num[3]))
    print('Denominad='+str(den[0])+','+str(den[1])+','+str(den[2])+','+str(den[3]))
    # print('Numerador='+str(tf1[0])+','+str(tf1[1])+','+str(tf1[2]))
    # print('Denominad='+str(tf1[3])+','+str(tf1[4])+','+str(tf1[5]))



