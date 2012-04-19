#when I'm trouble shooting and figuring out which index is which, etc. I'll try to leave in the code I was using as diagnostic

from __future__ import division
import  numpy as np
import scipy as sp
import scipy.signal
import getMDSplus


#the coils don't start up until about 5 seconds into the shot, so its normally a good idea to chop off the first 6 or 7 seconds (i.e. about 3000-4000 data points)
def startup(theData, startnum=4000):
    if theData['Tags']==False:
        print "tags must be specified for startupPrep"
        return False
    for tag in theData['Tags']:
        theData[tag]=theData[tag][startnum:,:]
    if "RespModes" in theData['Tags']  or "AppModes"in theData['Tags']:
        theData['Mtime']=theData['Mtime'][startnum:]
    if "Bfield" in theData['Tags'] or "Appfield" in theData['Tags'] or "RespField" in theData['Tags']:
        theData['Btime']=theData['Btime'][startnum:]
    #print theData['Bfield'].shape
    return theData

#removes the means from the signals. Normally do this relatively early
def fluctuation(theData):
    if theData['Tags']==False:
        print "tags must be specified for resamplePrep"
        return False
    for tag in theData['Tags']:
        nseries = theData[tag].shape[1]
        #print nseries
        means = np.mean(theData[tag], axis=0)
        #print means
        #print means.shape
        for i in np.arange(nseries):
            theData[tag][:,i] = [x - means[i] for x in theData[tag][:,i]]
        #print np.mean(theData[tag], axis=0)
    return theData



#this routine downsamples data using scipy.signal.resample, which maintains spectral accuracy.

def resample(theData, numsamples=32000, tags=False):
    if theData['Tags']==False:
        print "tags must be specified for resamplePrep"
        return False
    for tag in theData['Tags']:
        theData[tag] = sp.signal.resample(theData[tag], numsamples, axis =0)
    #modify the time tracker stuff
    if "RespModes" in theData['Tags']  or "AppModes"in theData['Tags']:
        theData['Mtime'] = sp.arange(min(theData['Mtime']), max(theData['Mtime']), (max(theData['Mtime'])-min(theData['Mtime']))/numsamples)
    if "Bfield" in theData['Tags'] or "Appfield" in theData['Tags'] or "RespField" in theData['Tags']:
        theData['Btime'] = sp.arange(min(theData['Btime']), max(theData['Btime']), (max(theData['Btime'])-min(theData['Btime']))/numsamples)
    return theData
