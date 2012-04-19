#This is for doing svd stuff within python. (clearly)
from __future__ import division
import  numpy as np
import scipy as sp
import scipy.linalg
from datetime import datetime
import getMDSplus
import dataPrep


#Type1 just appends all of the given data fields together and then takes the svd
def type1(shot, tags=['Bfield'], probesort=True, internal=True, external=False, numsamples=8000, startnum=4000):
    startTime = datetime.now()
    theData = getMDSplus.getData(shot, tags=tags, probesort=probesort, internal=internal, external=external)
    print "getMDSplus:" + str(datetime.now()-startTime)
    # for convenience, lets call the matrix to be SVDed A.
    theData = dataPrep.startup(theData, startnum=startnum)
    theData = dataPrep.fluctuation(theData)
    theData = dataPrep.resample(theData, numsamples, tags=tags)
    print "dataPrep:" + str(datetime.now()-startTime)
    A = theData[tags[0]]
    if len(tags)>1:
        for tag in tags[1:]:
            A = np.hstack(A, theData[tag])

    theData['U'], theData['s'], theData['Vh'] = sp.linalg.svd(A)
    print "SVD:" + str(datetime.now()-startTime)
    return theData
