from scipy import signal
def calcQandWo(transferFunction):
    tf = transferFunction
    num = [tf[0], tf[1], tf[2]]
    den = [tf[3],tf[4], tf[5]]
    wo = (den[0]/den[2])**-0.5
    Q = den[2]/(wo*den[1])
    return Q,wo

def calcK(Qo,Q):
    K = 1/(2*Qo**2) * (1-Qo/Q)+1
    return K

def calcKminusculaAndM(tf,Qo):
    Wz = (tf[2]/tf[0])**0.5
    Q,wo = calcQandWo(tf)
    n2 = tf[0]
    k = (n2*(Wz/wo)**2)/(1-Q/Qo)
    K = calcK(Qo,Q)
    M = k*((K-1)/K) * (1+2*Qo**2 * (wo/Wz)**2) 
    return k,M

def calcCapValues(C22preset,M):
    Cociente = M/(M-1)
    C21 = C22preset/ Cociente
    C3 = C21+C22preset
    return C21,C3


def calcWpAndQp(tf,Qo, WpoloDominante, Avol):
    Q,wo = calcQandWo(tf)
    wt = Avol * WpoloDominante
    wp = wo * (1+Qo*(wo/wt))
    temp = (1-(2*Qo*Q*(wo/wt)* (1/(2*Q) -wo/wt)) )
    Qp = Q * temp
    return wp,Qp

def calcG1andG41(C3Posta,C22Posta,C21Posta,Wp,Qo):
    G1 = 2*Qo*Wp* (C3Posta*(C22Posta+C21Posta))**0.5
    G41 = G1 /(4*Qo**2)
    return G1,G41


##Usamos por ahora TL082

wpolodominante = 10
Avol = 100e3
Qo = 4
wn = 2*3.1415 * 24.4E3
z,p,k = signal.ellip(4, 2, 40, wn, 'highpass', analog=True ,output='zpk')
hola = signal.zpk2sos(z, p, k)
tf1 = hola[0]
tf2 = hola[1]

Q1,Wo1 = calcQandWo(tf1)
Q2,Wo2 = calcQandWo(tf2)

print('Q1='+str(Q1) +'   Wo1='+str(Wo1))
print('Q2='+str(Q2) +'   Wo2='+str(Wo2))

K1 = calcK(Qo,Q1)
K2 = calcK(Qo,Q2)

print('')
print('K1='+str(K1)+'   K2='+str(K2))

kmin1, M1 = calcKminusculaAndM(tf1,Qo)
kmin2, M2 = calcKminusculaAndM(tf2,Qo)

print('')
print('kminuscula1='+ str(kmin1)+ '   M1='+str(M1))
print('kminuscula2='+ str(kmin2)+ '   M2='+str(M2))

C22preset = 10e-9
C21_1, C3_1 = calcCapValues(C22preset,M1)
C21_2, C3_2 = calcCapValues(C22preset,M2)

print('')
print('C21_1=' + str(C21_1)+'   C22_1='+str(C22preset)+ '   C3_1=' + str(C3_1))
print('C21_2=' + str(C21_2)+'   C22_2='+str(C22preset)+ '   C3_2=' + str(C3_2))

Wp1,Qp1 = calcWpAndQp(tf1,Qo,wpolodominante,Avol)
Wp2,Qp2 = calcWpAndQp(tf2,Qo,wpolodominante,Avol)


print('')
print('Wp1='+ str(Wp1)+'   Qp1='+str(Qp1))
print('Wp2='+ str(Wp2)+'   Qp2='+str(Qp2))

G1_1, G41_1 = calcG1andG41(C3_1,C22preset,C21_1,Wp1,Qo)
G1_2, G41_2 = calcG1andG41(C3_2,C22preset,C21_2,Wp2,Qo)

print('')
print('G1_1='+ str(G1_1)+'   G41_1='+ str(G41_1))
print('G1_2='+ str(G1_2)+'   G41_2='+ str(G41_2))







print('\n')