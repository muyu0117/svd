from __future__ import division
import numpy as np
import scipy as sp
import scipy.linalg
import matplotlib.pyplot as plt
import pylab as pl
#This just plots the basis of given number.
def plotBasis(theData, basis=0):
    fields = {'r':[], 't':[], 'p':[], 'rpos':[], 'tpos':[], 'ppos':[]}
    letters = ['r','t','p']
    colors = {'r':'red', 't':'blue', 'p':'green'}
    if 'Bfield' in theData['Tags']:
        for i in range(len(theData['Vh'][0,:])):
            for letter in letters:
                if letter in theData['Serials'][i]:
                    fields[letter].append(theData['Vh'][basis, i])
                    fields[letter+'pos'].append(theData['Position'][i][0]*np.sin(theData['Position'][i][2])/-.7071689)
    p={}
    pl.figure()
    for letter in letters:
        p[letter] = pl.plot(fields[letter+'pos'], fields[letter], color = colors[letter], label='B'+letter)
        pl.scatter(fields[letter+'pos'], fields[letter], color = colors[letter])
    pl.title('Internal Array Field for Basis #'+str(basis)+', sv='+str(theData['s'][basis]))
    pl.xlabel('r[m]')
    pl.ylabel('Relative B Field')
    pl.legend()

    #plot the timeseries
    pl.show()
