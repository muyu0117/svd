##------------------------------------------------------------------------------
##Routines that get MDSdata. Note that shots must be contained in  ~/Data/kilmernew/
##------------------------------------------------------------------------------
from __future__ import division
import  numpy as np
import scipy as sp
import MDSplus


##getBfield returns the Bfield array for a shot
def getBfield(shot):
    try:
        myTree=MDSplus.Tree('kilmernew', shot)
        Bfield=myTree.getNode('MEASUREMENTS:BFIELD').record.data()
        return Bfield
    except:
        return False

##getRespModes gets the external spherical harmonic response modes
def getRespModes(shot):
    try:
        myTree=MDSplus.Tree('kilmernew', shot)
        RespModes=myTree.getNode('ANALYSIS:RESP_MODES').record.data()
        return RespModes
    except:
        return False
##getAppModes gets the external spherical harmonic response modes
def getAppModes(shot):
    try:
        myTree=MDSplus.Tree('kilmernew', shot)
        RespModes=myTree.getNode('ANALYSIS:APP_MODES').record.data()
        return RespModes
    except:
        return False

##getSerials gets the list of ordered serials
def getSerials(shot):
    try:
        myTree = MDSplus.Tree('kilmernew', shot)
        serials = myTree.getNode('CALIBRATION.HALL_ARRAY:SERIAL').record.data()
        return serials.tolist()
    except:
        return False

##getPosition gets the list of ordered serials
def getPosition(shot):
    try:
        myTree = MDSplus.Tree('kilmernew', shot)
        Position = myTree.getNode('CALIBRATION.HALL_ARRAY:POSITION').record.data()
        return Position
    except:
        return False

def getGamma(shot):
    try:
        myTree = MDSplus.Tree('kilmernew', shot)
        gamma = myTree.getNode('ANALYSIS:GAMMA').record.data()
        return gamma
    except:
        return False
def getRawData(shot):
    try:
        myTree = MDSplus.Tree('kilmernew', shot)
        rawData = mytree.getNode('raw_data').record.data()
        return rawData
    except:
        return False

##getData takes the tags and populates the data dictionary
def getData(shot, tags=False,
            probesort=True, internal=True, external=False):
    if tags == False:
        print 'tags must be specified in getMDSplus.getData(tags="typetagshere")'
        return False
    if type(tags)==str:
        tags = [tags]
    data = {}
    data["Shot"] = shot
    data["Tags"] = tags
    if "RespModes" in tags  or "AppModes"in tags:
        data["gamma"] = getGamma(shot)
    if "RespModes" in tags:
        data["RespModes"] = getRespModes(shot)
        data["Mtime"] = sp.arange(0, max(data["RespModes"].shape)/512, 1/512)
    if "AppModes" in tags:
        data["AppModes"] = getRespModes(shot)
        data["Mtime"] = sp.arange(0, max(data["AppModes"].shape)/512, 1/512)
    if "Bfield" in tags:
        data["Bfield"] = getBfield(shot)
    if "Bfield" in tags or "Appfield" in tags or "RespField" in tags:
        data["Serials"] = getSerials(shot)
        data["Position"] = getPosition(shot)
        # a time field is created so that resampling can be kept track of within the dictionary
        data["Btime"] = sp.arange(0, max(data["Bfield"].shape)/512, 1/512)
        if probesort == True:
            probeSort(shot, data, internal=internal, external=external)
    if "RawData" in tags:
        data["RawData"] = getRawData(shot)
    return data

#goodProbes gives a list of goodprobes
#the ordering of the probes here determines the ordering in the fields returned by probeSort, so put this how you want it and stuff
def goodProbes(shot, internal=True, external=False):
    probes=[]
    if external == True:
        probes +=[
        'HP001 ', 'HP002 ', 'HP003 ', 'HP004 ', 'HP005 ', 'HP006 ',
        'HP007 ', 'HP008 ', 'HP009 ', 'HP010 ', 'HP011 ', 'HP012 ',
        'HP013 ', 'HP014 ', 'HP015 ', 'HP016 ', 'HP017 ', 'HP018 ',
        'HP019 ', 'HP020 ', 'HP021 ', 'HP022 ', 'HP023 ', 'HP024 ',
        'HP025 ', 'HP026 ', 'HP027 ', 'HP028 ', 'HP029 ', 'HP030 ',
        'HP031 ', 'HP032 ', 'HP033 ', 'HP034 ', 'HP035 ', 'HP036 ',
        'HP037 ', 'HP038 ', 'HP039 ', 'HP040 ', 'HP041 ', 'HP042 ',
        'HP043 ', 'HP044 ', 'HP045 ', 'HP046 ', 'HP047 ', 'HP048 ',
        'HP049 ', 'HP050 ', 'HP051 ', 'HP052 ', 'HP053 ', 'HP054 ',
        'HP055 ', 'HP056 ', 'HP057 ', 'HP058 ', 'HP059 ', 'HP060 ',
        'HP061 ', 'HP062 ', 'HP063 ', 'HP064 ', 'HP065 ', 'HP066 ',
        'HP067 ', 'HP068 ', 'HP069 ', 'HP070 ', 'HP071 ', 'HP072 ',
        'HP073 ', 'HP074 ', 'HP075 ', 'HP076 ']
    if str(shot)[0:6] == '110929':
        if internal == True:
            probes +=[
'HP100p','HP101p','HP102p','HP103p','HP104p','HP105p','HP106p','HP107p', 'HP108p', 'HP109p',
'HP110p','HP111p','HP112p','HP114p','HP115p','HP117p',
'HP121p','HP122p','HP123p','HP125p','HP126p','HP127p', 'HP128p', 'HP129p',
'HP130p','HP131p','HP132p','HP134p','HP135p','HP137p', 'HP139p',
'HP100r','HP101r','HP102r','HP103r','HP104r','HP105r','HP106r','HP107r', 'HP108r', 'HP109r',
'HP111r','HP113r','HP114r','HP116r','HP117r', 'HP118r', 'HP119r',
'HP120r','HP121r','HP123r','HP125r','HP126r','HP127r','HP129r',
'HP131r','HP132r','HP134r','HP136r', 'HP139r',
'HP100t','HP101t','HP102t','HP103t','HP104t','HP105t','HP106t','HP107t', 'HP108t', 'HP109t',
'HP110t','HP111t','HP112t','HP113t','HP114t','HP115t','HP116t','HP117t', 'HP118t', 'HP119t',
'HP121t','HP122t','HP123t','HP124t','HP125t','HP126t','HP127t', 'HP128t',
'HP130t','HP131t','HP132t','HP133t','HP134t','HP135t','HP137t', 'HP139t']
    return probes

##probeSort limits the bfield type tags to goodprobes as specified by the serials in the goodProbes function
def probeSort(shot, data, internal=True, external=False):
    fieldtags = ['Bfield', 'App_Field', 'Resp_Field']
    serials = data["Serials"]
    goodSerials = goodProbes(shot, internal=internal, external=external)
    for tag in data.keys():
        if tag in fieldtags:
            inds = []
            for serial in goodSerials:
                inds.append(serials.index(serial))
            data[tag] = data[tag][:,inds]
    data['Serials'] = goodSerials
    data['Position'] = data['Position'][inds, :]
