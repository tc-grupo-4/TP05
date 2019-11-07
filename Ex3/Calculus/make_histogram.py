# coding=utf-8
from computar_maximos import computar_notch
from read_spice_montecarlo import read_file_spice
import seaborn as sns
import matplotlib.pyplot as plt
from datacursor_easy import make_datacursor_general
from distutils.spawn import find_executable

def make_histogram(variable, unidad, data, filename, bar_width):
    
    if variable=="Fo":
        ax1 = sns.distplot(data, norm_hist=True,kde_kws={"color":"#FF9730","lw": 3},hist_kws={"color":"#D16800","alpha": 0.9})
        

    elif variable=="Q":
        ax1 = sns.distplot(data, norm_hist=True,kde_kws={"color":"#0073D3","lw": 3},hist_kws={"color":"#5CB5FF","alpha": 0.9})
    
    y_vals = ax1.get_yticks()

    ax1.set_yticklabels(['{:3.0f}%'.format(x * 100 * bar_width) for x in y_vals])
    if find_executable("latex") is not None:
        plt.rc('font',**{'family':'serif','serif':['Palatino']})
        plt.rc('text', usetex=True)
    plt.xlabel(variable+" ["+unidad+"]")
    plt.ylabel("% de ocurrencias")
    #print(find_executable("latex"))
    

    #plt.show()
 
    make_datacursor_general(
        x1= variable,
        u1= unidad,
        filename=filename,
        my_plt=plt,
        ax1=ax1)

    plt.cla()
    plt.close()





