##------------------------------------------------------------------------------
##Routines that get specified data for a given shot number for an already open
##mdsplus server
##M. Brookhart 8/27/2010
##------------------------------------------------------------------------------
import numpy as np
import MDSplus

##------------------------------------------------------------------------------
##getAnodeCurrents returns Segmented Anode Currents for a shot
##------------------------------------------------------------------------------

def getAnodeCurrents(shot):
    try:
        myTree=MDSplus.Tree('rwm',shot)

        Center=myTree.getNode('.ANODE.I_CENTER_DOT').record.data()
        Inner=myTree.getNode('.ANODE.I_INNER_RING').record.data()
        Outer=myTree.getNode('.ANODE.I_OUTER_RING').record.data()
        t=myTree.getNode('.ANODE.I_CENTER_DOT').getDimensionAt().data()
        if 1:
            ds=5
            Center=Center[0::ds]
            Inner=Inner[0::ds]
            Outer=Outer[0::ds]
            t=t[0::ds]

        return True,Center,Inner,Outer,t
    except:
        return False,0,0,0,0
##------------------------------------------------------------------------------
##getArcSigs takes the shot number and returns I Bias & V Bias for all guns
##------------------------------------------------------------------------------
def getArcSigs(shot):
    myTree=MDSplus.Tree('rwm',shot)

    Vn='.gun.voltage:V_'
    In='.gun.current:I_'
    if shot<110919000:n=24000
    else: n=25000
    V=np.empty((n,19))
    I=np.empty((n,19))
    for i in range(1,20):
        V[:,i-1]=myTree.getNode(Vn+str(i)).record.data()
        I[:,i-1]=myTree.getNode(In+str(i)).record.data()
    I_t=myTree.getNode('.gun:bias_current:IB_10').getDimensionAt().data()
    V_t=myTree.getNode('.gun:bias_voltage:VB_10').getDimensionAt().data()

    return I,I_t,V,V_t
##------------------------------------------------------------------------------
##getBiasSigs takes the shot number and returns I Bias & V Bias for all guns
##------------------------------------------------------------------------------
def getBiasSigs(shot):
    myTree=MDSplus.Tree('rwm',shot)

    Vn='.gun.bias_voltage:VB_'
    In='.gun.bias_current:IB_'
    if shot<110919000:n=24000
    else: n=25000
    VB=np.empty((n,19))
    IB=np.empty((n,19))
    for i in range(1,20):
        VB[:,i-1]=myTree.getNode(Vn+str(i)).record.data()
        IB[:,i-1]=myTree.getNode(In+str(i)).record.data()

    I_t=myTree.getNode('.gun:bias_current:IB_10').getDimensionAt().data()
    V_t=myTree.getNode('.gun:bias_voltage:VB_10').getDimensionAt().data()

    return IB,I_t,VB,V_t
##------------------------------------------------------------------------------
##getBr takes the shot number and Returns Bz from S
##------------------------------------------------------------------------------
def getBr(shot):
    if shot<110919000:n=24000
    else: n=25000
    if shot==0:n=25000
    names=getBrNames()
    myTree=MDSplus.Tree('rwm',shot)
    Br=np.empty((n,8,10))
    for i in range(8):
        for j in range(10):
            Br[:,i,j]=myTree.getNode('.MAG.BR_80_LOOP.'+names[i,j]
                                    ).record.data()
    t=myTree.getNode('.MAG.BR_80_LOOP.A101').getDimensionAt().data()
    inv=getBrInv()
    Br=Br*inv
    return Br,t
##------------------------------------------------------------------------------
##getBr takes the shot number and Returns Bz from S
##------------------------------------------------------------------------------
def getBrNames():
    #Kapton Array Mapping
    names=np.array([
        ['b13', 'b21','b24','b22', 'b23', 'b31', 'b34', 'b11', 'b14', 'b12' ],
        ['b63', 'b71','b74','b72', 'b73', 'b81', 'b84', 'b61', 'b64', 'b62' ],
        ['b53', 'b41','b44','b42', 'b43', 'b32', 'b33', 'b51', 'b54', 'b52' ],
        ['b104','b91','b94','b92', 'b93', 'b82', 'b83', 'b101','b103','b102'],
        ['a93', 'a92','a91','a104','a103','a102','a101','a84', 'a83', 'a94' ],
        ['a43', 'a42','a41','a54', 'a53', 'a52', 'a51', 'a34', 'a33', 'a44' ],
        ['a73', 'a72','a71','a64', 'a63', 'a62', 'a61', 'a82', 'a81', 'a74' ],
        ['a23', 'a22','a21','a14', 'a13', 'a12', 'a11', 'a32', 'a31', 'a24' ]
                ],dtype='S4')
    names=names[::-1]
    return names
##------------------------------------------------------------------------------
##getBrInv returns the polarity of the old Br Array
##------------------------------------------------------------------------------
def getBrInv():
    inv=np.array([
           [ 1,  1, -1,  1,  1,  1, -1,  1, -1,  1],
           [ 1,  1, -1,  1,  1,  1, -1,  1, -1,  1],
           [ 1,  1, -1,  1,  1,  1,  1,  1, -1,  1],
           [ 1,  1, -1,  1,  1,  1,  1,  1, -1,  1],
           [ 1, -1,  1,  1,  1, -1,  1,  1,  1,  1],
           [ 1, -1,  1,  1,  1, -1,  1,  1,  1,  1],
           [ 1, -1,  1,  1,  1, -1,  1, -1,  1,  1],
           [ 1, -1,  1,  1,  1, -1,  1, -1,  1,  1]])
    inv=inv[::-1]
    return inv
##------------------------------------------------------------------------------
##getBz takes the shot number and Returns Bz from S
##------------------------------------------------------------------------------
def getBzEq(shot):
    myTree=MDSplus.Tree('rwm',shot)

    IRex=myTree.getNode('.THUMBS.I_REX').record.data()
    Bz0=IRex.mean()*3.929 #convert from A to Bz

    return Bz0
##------------------------------------------------------------------------------
##getBz takes the shot number and Returns Bz from S
##------------------------------------------------------------------------------
def getGTOSigs(shot):
    myTree=MDSplus.Tree('dtacq0',shot)
    GTO=np.empty((7,25000))
    for i in range(77,84):
        GTO[i-77]=myTree.getNode('.CH'+str(i)).record.data()
    t=myTree.getNode('.CH'+str(i)).getDimensionAt().data()*2
    return GTO,t

##------------------------------------------------------------------------------
##getLang takes the shot number and Returns Langmuir Probe Tips
##------------------------------------------------------------------------------
def getLang(shot):
    myTree=MDSplus.Tree('rwm',shot)

    z=myTree.getNode('.langmuir.d').record.data()
    Theta=myTree.getNode('.langmuir.phi').record.data()

    myNode=myTree.getNode('.LANGMUIR.VF')
    VF=myNode.record.data()
    t=myNode.getDimensionAt().data()

    return z,Theta,VF,t
##------------------------------------------------------------------------------
##getMachProbe takes the shot number and returns data from MDSplus
##------------------------------------------------------------------------------
def getMachSigs(shot):
    myTree=MDSplus.Tree('rwm',shot)

    #get values from mdsplus
    tip1=myTree.getNode('.mach.tip2').record.data()[0:24000] #Tips are switched in dataloop20.pro, reswitching here
    tip2=myTree.getNode('.mach.tip1').record.data()[0:24000]
    t=myTree.getNode('.mach.tip1').getDimensionAt().data()[0:24000]
    z=myTree.getNode('.mach.z').record.data()
    theta=myTree.getNode('.mach.theta').record.data()
    vBias=myTree.getNode('.mach.vbias').record.data()[0:24000]

    #remove spurious values
    tip1[0]=0
    tip2[0]=0

    return z,theta,vBias.tolist(),tip1.tolist(),tip2.tolist(),t
##------------------------------------------------------------------------------
##getSingleBtheta takes the shot number and returns
##B_theta from a single reference coil
##Mostly used for correlation analysis stuff
##------------------------------------------------------------------------------
def getSingleBtheta(shot):
    myTree=MDSplus.Tree('rwm',shot)

    Bint=myTree.getNode('.mag.sia:A_3').record.data()[0:12000]
    t=t=myTree.getNode('.mag.sia:A_3').getDimensionAt().data()[0:24000]

    Bint[0]=0
    Bint=np.squeeze(Bint)

    return Bint,t
##------------------------------------------------------------------------------
##getTriBdot takes the shot number and returns data from MDSplus
##------------------------------------------------------------------------------
def getTriBdot(shot):
    #open the tree
    myTree=MDSplus.Tree('rwm',shot)

    #get values from mdsplus
    Bcoil1=myTree.getNode('bdot.coil1').record.data()
    Bcoil2=myTree.getNode('bdot.coil2').record.data()
    Bcoil3=myTree.getNode('bdot.coil3').record.data()
    t=myTree.getNode('bdot.coil1').getDimensionAt().data()
    z=myTree.getNode('.bdot.z').record.data()
    Theta=myTree.getNode('.bdot.theta').record.data()
    #remove spurious values
    Bcoil1[0]=0
    Bcoil2[0]=0
    Bcoil3[0]=0

    return z,Theta,Bcoil1,Bcoil2,Bcoil3,t
def getVSP(shot):
    VSP=[]
    VSP+=[MDSplus.Tree('dtacq0',shot).getNode('.CH93').getData().data().mean()]
    VSP+=[MDSplus.Tree('dtacq0',shot).getNode('.Ch94').getData().data().mean()]
    return VSP
