import SpiceParser as sp 


filePath = "cambiar.txt"
parser = sp.SpiceParser()
freq, mag, phase = parser.parseSpiceFile(filePath)

outF=open("SALIDA.csv","w+")
outF.write("Frecuency (Hz), Magnitude (Ohms), Phase (°)\n")
for i in range(0,len(freq)):
    outF.write(str(freq[i])+','+str(10**(mag[i]/20))+','+str(phase[i])+'\n')
outF.close()