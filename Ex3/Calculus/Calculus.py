from scipy import signal
import pprint
import numpy as np
from numpy import pi
from eseries import find_nearest, E12,E24,E48
import time
import control as cl
import matplotlib.pyplot as plt
from SpiceParser import SpiceParser 
import matplotlib.pyplot as plt

def plotPolesAndZeros(tf):
    num = [tf[0] , tf[1], tf[2]]
    den = [tf[3] , tf[4], tf[5]]
    sistema = cl.TransferFunction(num,den)
    cl.pzmap(sistema,Plot=True)
    plt.show()
    return


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

    def exportToSpice(self, file, cellnumber):
        textList=[]
        index=0
        for key, value in self.values.items():
            index=index+1
            textList.append("TEXT "+str(384+300*cellnumber)+" "+str(736+index*50)+" Left 2 !.param "+str(key)+"_"+str(cellnumber)+" "+str(value))
        for line in textList:
            file.write(line)
            file.write("\n")
    
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

    def roundValues(self,NormRes, NormCap):
        roundingNorm = NormRes
        roundingNormCap = NormCap
        self.values['C21'] = find_nearest(roundingNormCap,self.values['C21'])
        self.values['C22'] = find_nearest(roundingNormCap,self.values['C22'])
        self.values['C3'] = find_nearest(roundingNormCap,self.values['C3'])
        self.values['Ra1'] = find_nearest(roundingNorm,self.values['Ra1'])
        self.values['Ra2'] = find_nearest(roundingNorm,self.values['Ra2'])
        self.values['R41'] = find_nearest(roundingNorm,self.values['R41'])
        self.values['R42'] = find_nearest(roundingNorm,self.values['R42'])
        self.values['R1'] = find_nearest(roundingNorm,self.values['R1'])
        self.values['Rb'] = find_nearest(roundingNorm,self.values['Rb'])



if __name__ == "__main__":
    ##Empeze a usar el LM833 porque tiene mejor GBP y el TL082 la cagaba en las siulaciones
    wpolodominante = 11
    Avol = 316227
    wp = 2*pi * 23E3               ##no tocar estos valores q anda re piola guachin
    wa = 2*pi * 13E3
    wpn = 1
    wan = wp/wa
    Aa = 45
    Ap = 1
    Rb = 1e3
    C = 5e-9
    Round = False
    Montecarlo = False
    ExportarLTSpice = False
    plot=True
    plotSpice=True
    spiceFile=False
    
    if spiceFile is True:
        parser=SpiceParser()
        if parser.parseSpiceFile(filePath="spicetxt.txt") != -1:
            wspice, magspice, phasespice = parser.parseSpiceFile("spicetxt.txt")
        else:
            spiceFile=False

    n,wn = signal.ellipord(wpn,wan,Ap,Aa,analog=True)
    if n > 4:
        print("No es posible hacerlo de orden 4")
    else:
        z,p,k = signal.ellip(n, Ap, Aa, wn, 'lowpass', analog=True, output='zpk')
        test = p[0] +1j
        z,p,k = signal.lp2hp_zpk(z,p,k,wp)
        # num,den = signal.ellip(n, Ap, Aa, wn, 'lowpass', analog=True)
        # num,den = signal.lp2hp(num,den,wp)
        # sistema = cl.TransferFunction(num,den)
        # cl.pzmap(sistema,Plot=True)
        # plt.show()
        TransferFunction = signal.zpk2sos(z, p, k)
        tf1 = TransferFunction[0]
        # plotPolesAndZeros(tf1)
        tf2 = TransferFunction[1]
        # plotPolesAndZeros(tf2)

        Etapa1 = Sedra(wpolodominante,Avol,Rb,C,tf1,'ETAPA 1')
        Etapa2 = Sedra(wpolodominante,Avol,Rb,C,tf2,'ETAPA 2')

        if plot is True:
            b, a = signal.ellip(n, Ap, Aa, wn, 'lowpass', analog=True)
            w, h = signal.freqs(b, a)
            plt.semilogx(w, 20 * np.log10(abs(h)))
            plt.title('Elliptic filter frequency response')
            plt.xlabel('Frequency')
            plt.ylabel('Amplitude [dB]')
            plt.margins(0, 0.1)
            plt.grid(which='both', axis='both')
            plt.axvline(wn, color='green') # cutoff frequency
            plt.axhline(-Aa, color='green') # rs
            plt.axhline(-Ap, color='green') # rp
            if spiceFile and plotSpice:
                plt.semilogx(wspice, magspice)
                plt.semilogx(wspice, phasespice)  # Bode phase plot
            plt.show()

        #Etapa1.printFilterValues()
        if Round is True:
            Etapa1.roundValues(E24,E12)
        Etapa1.printComponentValues()

        #Etapa2.printFilterValues()
        if Round is True:
            Etapa2.roundValues(E24,E12)
        Etapa2.printComponentValues()

        ## Solo para mi despues queda comentado
        num,den = signal.zpk2tf(z,p,k)#signal.ellip(n, Ap, Aa, wn, 'highpass', analog=True)
        print('Numerador=  '+str(num[0])+','+str(num[1])+','+str(num[2])+','+str(num[3])+','+str(num[4]))
        print('Denominad=  '+str(den[0])+','+str(den[1])+','+str(den[2])+','+str(den[3])+','+str(den[4]))
        #print('Numerador='+str(tf2[0])+','+str(tf2[1])+','+str(tf2[2]))
        #print('Denominad='+str(tf2[3])+','+str(tf2[4])+','+str(tf2[5]))
        
        if ExportarLTSpice is True:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            if Montecarlo is False:
                inF = open("simulation_template.asc", "r")
            else:
                inF = open("simulation_template2.asc", "r")
            outF=open("simulation_generated_"+timestr+".asc","w+")
            outF.write(inF.read())
            Etapa1.exportToSpice(outF,1)
            Etapa2.exportToSpice(outF,2)
            outF.close()
            inF.close()
