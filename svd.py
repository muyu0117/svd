#This is for doing svd stuff within python.
import  numpy as np
import scipy as sp
import getMDSplus



##getData calls the needed data from the MDSplus trees
def getData(shot, tags=["Bfield"], probesort=True, internal=True, external=False):
    try:
        data = getMDSplus.getData(shot, tags=tags)
        return data
    except:
        return False
