from scipy import signal
wn = 2*3.1415 * 24.4E3
z,p,k = signal.ellip(4, 2, 40, wn, 'highpass', analog=True ,output='zpk')
hola = signal.zpk2sos(z, p, k)
tf1 = hola[0]
tf2 = hola[1]