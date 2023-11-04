from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, ConvertToDlString, SetAddonStatus, FirstFreeIdNumber, insertSpaces
from RFEM.BasicObjects.node import Node

from RFEM.LoadCasesAndCombinations.loadCase import LoadCase

from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Loads.freeLoad import FreeLoad
from RFEM.Calculate.meshSettings import GetModelInfo
# from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf

from MFE_ALG import *

def WindFreeRecLoad(LC:int = 1,
                    surfaces: str="1",
                    projection: str="XY",
                    load: float=1.0,                # in kN/m2
                    points: list=[0.0,0.0,1.0,1.0], # coördintaten in meters
                    comment: str="TestComment",
                    model = Model):

    if projection == "XY": FrLoadProj = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV
    elif projection == "XZ": FrLoadProj = FreeLoadLoadProjection.LOAD_PROJECTION_XZ_OR_UW
    elif projection == "YZ": FrLoadProj = FreeLoadLoadProjection.LOAD_PROJECTION_YZ_OR_VW

    points.append(0)

    FreeLoad.RectangularLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_RECTANGULAR_LOAD,LC),
                             LC,surfaces,FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                             FrLoadProj,FreeRectangularLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                             [load*1000],FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                             points,comment)


def Wind(
        qpz : float = 1.11,
        Lx : float = 10,
        Ly : float = 20,
        h : float = 5,
        h_dr : float = 0.5,
        dhr : float = 0.2,
        BaseNodeNo : int = 1,
        model = Model
        ):
    b=[Ly,Lx]
    d=[Lx,Ly]

    # lijst met waarden Cpe opstellen
    h_d = [h/d[0],h/d[1]]
    cpeE=[0.0, 0.0]
    for i in range(2):
        if h_d[i]<=1: cpeE[i] = -0.5
        elif h_d[i]>=5: cpeE[i] = -0.7
        else: cpeE[i] = interpol(h_d[i],1,5,-0.5,-0.8)

    if dhr/h <0.025:
        cpeF = interpol(dhr/h,0,0.025,-1.8,-1.6)
        cpeG = interpol(dhr/h,0,0.025,-1.2,-1.1)
    elif dhr/h <0.05:
        cpeF = interpol(dhr/h,0.025,0.05,-1.6,-1.4)
        cpeG = interpol(dhr/h,0.025,0.05,-1.1,-0.9)
    elif dhr/h <0.10:
        cpeF = interpol(dhr/h,0.05,0.10,-1.4,-1.2)
        cpeG = interpol(dhr/h,0.05,0.10,-0.9,-0.8)
    else:
        cpeF = -1.2
        cpeG = -0.8

    cpeH = -0.7
    cpeId = 0.2
    cpeIz = -0.2

    e=[min(b[0],2*h),min(b[1],2*h)]
    cpe = [-1.2,-0.8,-0.5,0.8,cpeE,cpeF,cpeG,cpeH,cpeId,cpeIz]

    cpe_str = []
    for c in range(4):
        if cpe[c]>0: cpe_str.append("+" + str(cpe[c]))
        else: cpe_str.append(str(cpe[c]))
    cpe_str.append([])
    for c in range(2):
        if cpe[4][c]>0: cpe_str[4].append("+" + str(cpe[4][c]))
        else: cpe_str[4].append(str(cpe[4][c]))
    for c in range(5,10):
        if cpe[c]>0: cpe_str.append("+" + str(cpe[c]))
        else: cpe_str.append(str(cpe[c]))
    print(cpe_str)

    # Lijst met boven- en ondergrens Cpi opstellen
    # TODO: Kijken of dit wel klopt en of het niet eigenlijk met figuur 7.13 van 1991-1-4 moet worden bepaald.

    cpi = [0.2,-0.3]
    cpi_str_inv = ["-0.2","+0.3"]


    W_A = [qpz*(cpe[0]-cpi[0]),qpz*(cpe[0]-cpi[1]),""]
    W_B = [qpz*(cpe[1]-cpi[0]),qpz*(cpe[1]-cpi[1])]
    W_C = [qpz*(cpe[2]-cpi[0]),qpz*(cpe[2]-cpi[1])]
    W_D = [qpz*(cpe[3]-cpi[0]),qpz*(cpe[3]-cpi[1])]
    W_Ex = [qpz*(cpe[4][0]-cpi[0]),qpz*(cpe[4][0]-cpi[1])]
    W_Ey = [qpz*(cpe[4][1]-cpi[0]),qpz*(cpe[4][1]-cpi[1])]
    W_F = [qpz*(cpe[5]-cpi[0]),qpz*(cpe[5]-cpi[1])]
    W_G = [qpz*(cpe[6]-cpi[0]),qpz*(cpe[6]-cpi[1])]
    W_H = [qpz*(cpe[7]-cpi[0]),qpz*(cpe[7]-cpi[1])]
    W_Id = qpz*(cpe[8]-cpi[1])
    W_Iz = qpz*(cpe[9]-cpi[0])

    Model.clientModel.service.begin_modification()

    BaseNode = Node.GetNode(BaseNodeNo,model)
    xb = BaseNode.coordinate_1
    yb = BaseNode.coordinate_2
    zb = BaseNode.coordinate_3

#Wind +X OVERDRUK
    WindFreeRecLoad(401,"4 5","XZ",W_A[0],[xb,yb,xb+e[0]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[0] + ") = " + str(round(W_A[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"4 5","XZ",W_B[0],[xb+e[0]/5,yb,xb+e[0],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[0] + ") = " + str(round(W_B[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"4 5","XZ",W_C[0],[xb+e[0],zb,xb+d[0],zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[0] + ") = " + str(round(W_C[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"2","YZ",W_D[0],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[0] + ") = " + str(round(W_D[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"3","YZ",W_Ex[0],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[4][0] + cpi_str_inv[0] + ") = " + str(round(W_Ex[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"1","XY",W_F[0],[xb,yb,xb+e[0]/10,yb+e[0]/4],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"1","XY",W_F[0],[xb,yb+b[0],xb+e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"1","XY",W_G[0],[xb,yb+e[0]/4,xb+e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[0] + ") = " + str(round(W_G[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"1","XY",W_H[0],[xb+e[0]/10,yb,xb+e[0]/2,yb+b[0]],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[0] + ") = " + str(round(W_H[0],2)) + " kN/m²")
    WindFreeRecLoad(401,"1","XY",W_Iz,[xb+e[0]/2,yb,xb+d[0],yb+b[0]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[0] + ") = " + str(round(W_Iz,2)) + " kN/m²")

#Wind -X OVERDRUK
    WindFreeRecLoad(402,"4 5","XZ",W_A[0],[xb+d[0],yb,xb+d[0]-e[0]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[0] + ") = " + str(round(W_A[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"4 5","XZ",W_B[0],[xb+d[0]-e[0]/5,yb,xb+d[0]-e[0],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[0] + ") = " + str(round(W_B[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"4 5","XZ",W_C[0],[xb+d[0]-e[0],zb,xb,zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[0] + ") = " + str(round(W_C[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"3","YZ",W_D[0],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[0] + ") = " + str(round(W_D[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"2","YZ",W_Ex[0],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[4][0] + cpi_str_inv[0] + ") = " + str(round(W_Ex[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"1","XY",W_F[0],[xb+d[0],yb,xb+d[0]-e[0]/10,yb+e[0]/4],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"1","XY",W_F[0],[xb+d[0],yb+b[0],xb+d[0]-e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"1","XY",W_G[0],[xb+d[0],yb+e[0]/4,xb+d[0]-e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[0] + ") = " + str(round(W_G[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"1","XY",W_H[0],[xb+d[0]-e[0]/10,yb,xb+d[0]-e[0]/2,yb+b[0]],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[0] + ") = " + str(round(W_H[0],2)) + " kN/m²")
    WindFreeRecLoad(402,"1","XY",W_Iz,[xb+d[0]-e[0]/2,yb,xb,yb+b[0]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[0] + ") = " + str(round(W_Iz,2)) + " kN/m²")

#Wind +Y OVERDRUK
    WindFreeRecLoad(403,"2 3","YZ",W_A[0],[yb,zb,yb+e[1]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[0] + ") = " + str(round(W_A[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"2 3","YZ",W_B[0],[yb+e[1]/5,zb,yb+e[1],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[0] + ") = " + str(round(W_B[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"2 3","YZ",W_C[0],[yb+e[1],zb,yb+d[1],zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[0] + ") = " + str(round(W_C[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"4","XZ",W_D[0],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[0] + ") = " + str(round(W_D[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"5","XZ",W_Ey[0],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[4][1] + cpi_str_inv[0] + ") = " + str(round(W_Ey[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"1","XY",W_F[0],[xb,yb,xb+e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"1","XY",W_F[0],[xb+b[1],yb,xb+b[1]-e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"1","XY",W_G[0],[xb+e[1]/4,yb,xb+b[1]-e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[0] + ") = " + str(round(W_G[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"1","XY",W_H[0],[xb,yb+e[1]/10,xb+b[1],yb+e[1]/2],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[0] + ") = " + str(round(W_H[0],2)) + " kN/m²")
    WindFreeRecLoad(403,"1","XY",W_Iz,[xb,yb+e[1]/2,xb+b[1],yb+d[1]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[0] + ") = " + str(round(W_Iz,2)) + " kN/m²")

# #Wind -Y OVERDRUK
    WindFreeRecLoad(404,"2 3","YZ",W_A[0],[yb+d[1],zb,yb+d[1]-e[1]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[0] + ") = " + str(round(W_A[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"2 3","YZ",W_B[0],[yb+d[1]-e[1]/5,zb,yb+d[1]-e[1],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[0] + ") = " + str(round(W_B[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"2 3","YZ",W_C[0],[yb+d[1]-e[1],zb,yb,zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[0] + ") = " + str(round(W_C[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"5","XZ",W_D[0],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[0] + ") = " + str(round(W_D[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"4","XZ",W_Ey[0],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[4][1] + cpi_str_inv[0] + ") = " + str(round(W_Ey[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"1","XY",W_F[0],[xb,yb+d[1],xb+e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"1","XY",W_F[0],[xb+b[1],yb+d[1],xb+b[1]-e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[0] + ") = " + str(round(W_F[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"1","XY",W_G[0],[xb+e[1]/4,yb+d[1],xb+b[1]-e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[0] + ") = " + str(round(W_G[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"1","XY",W_H[0],[xb,yb+d[1]-e[1]/10,xb+b[1],yb+d[1]-e[1]/2],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[0] + ") = " + str(round(W_H[0],2)) + " kN/m²")
    WindFreeRecLoad(404,"1","XY",W_Iz,[xb,yb+d[1]-e[1]/2,xb+b[1],yb],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[0] + ") = " + str(round(W_Iz,2)) + " kN/m²")

#Wind +X ONDERDRUK
    WindFreeRecLoad(411,"4 5","XZ",W_A[1],[xb,yb,xb+e[0]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[1] + ") = " + str(round(W_A[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"4 5","XZ",W_B[1],[xb+e[0]/5,yb,xb+e[0],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[1] + ") = " + str(round(W_B[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"4 5","XZ",W_C[1],[xb+e[0],zb,xb+d[0],zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[1] + ") = " + str(round(W_C[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"2","YZ",W_D[1],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[1] + ") = " + str(round(W_D[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"3","YZ",W_Ex[1],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[4][0] + cpi_str_inv[1] + ") = " + str(round(W_Ex[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"1","XY",W_F[1],[xb,yb,xb+e[0]/10,yb+e[0]/4],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"1","XY",W_F[1],[xb,yb+b[0],xb+e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"1","XY",W_G[1],[xb,yb+e[0]/4,xb+e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[1] + ") = " + str(round(W_G[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"1","XY",W_H[1],[xb+e[0]/10,yb,xb+e[0]/2,yb+b[0]],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[1] + ") = " + str(round(W_H[1],2)) + " kN/m²")
    WindFreeRecLoad(411,"1","XY",W_Id,[xb+e[0]/2,yb,xb+d[0],yb+b[0]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[1] + ") = " + str(round(W_Id,2)) + " kN/m²")

#Wind -X ONDERDRUK
    WindFreeRecLoad(412,"4 5","XZ",W_A[1],[xb+d[0],yb,xb+d[0]-e[0]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[1] + ") = " + str(round(W_A[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"4 5","XZ",W_B[1],[xb+d[0]-e[0]/5,yb,xb+d[0]-e[0],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[1] + ") = " + str(round(W_B[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"4 5","XZ",W_C[1],[xb+d[0]-e[0],zb,xb,zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[1] + ") = " + str(round(W_C[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"3","YZ",W_D[1],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[1] + ") = " + str(round(W_D[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"2","YZ",W_Ex[1],[yb,zb,yb+b[0],zb+h],str(qpz) + "·(" + cpe_str[4][0] + cpi_str_inv[1] + ") = " + str(round(W_Ex[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"1","XY",W_F[1],[xb+d[0],yb,xb+d[0]-e[0]/10,yb+e[0]/4],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"1","XY",W_F[1],[xb+d[0],yb+b[0],xb+d[0]-e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"1","XY",W_G[1],[xb+d[0],yb+e[0]/4,xb+d[0]-e[0]/10,yb+b[0]-e[0]/4],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[1] + ") = " + str(round(W_G[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"1","XY",W_H[1],[xb+d[0]-e[0]/10,yb,xb+d[0]-e[0]/2,yb+b[0]],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[1] + ") = " + str(round(W_H[1],2)) + " kN/m²")
    WindFreeRecLoad(412,"1","XY",W_Id,[xb+d[0]-e[0]/2,yb,xb,yb+b[0]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[1] + ") = " + str(round(W_Id,2)) + " kN/m²")

#Wind +Y ONDERDRUK
    WindFreeRecLoad(413,"2 3","YZ",W_A[1],[yb,zb,yb+e[1]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[1] + ") = " + str(round(W_A[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"2 3","YZ",W_B[1],[yb+e[1]/5,zb,yb+e[1],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[1] + ") = " + str(round(W_B[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"2 3","YZ",W_C[1],[yb+e[1],zb,yb+d[1],zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[1] + ") = " + str(round(W_C[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"4","XZ",W_D[1],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[1] + ") = " + str(round(W_D[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"5","XZ",W_Ey[1],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[4][1] + cpi_str_inv[1] + ") = " + str(round(W_Ey[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"1","XY",W_F[1],[xb,yb,xb+e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"1","XY",W_F[1],[xb+b[1],yb,xb+b[1]-e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"1","XY",W_G[1],[xb+e[1]/4,yb,xb+b[1]-e[1]/4,yb+e[1]/10],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[1] + ") = " + str(round(W_G[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"1","XY",W_H[1],[xb,yb+e[1]/10,xb+b[1],yb+e[1]/2],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[1] + ") = " + str(round(W_H[1],2)) + " kN/m²")
    WindFreeRecLoad(413,"1","XY",W_Id,[xb,yb+e[1]/2,xb+b[1],yb+d[1]],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[1] + ") = " + str(round(W_Id,2)) + " kN/m²")

# #Wind -Y ONDERDRUK
    WindFreeRecLoad(414,"2 3","YZ",W_A[1],[yb+d[1],zb,yb+d[1]-e[1]/5,zb+h],str(qpz) + "·(" + cpe_str[0] + cpi_str_inv[1] + ") = " + str(round(W_A[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"2 3","YZ",W_B[1],[yb+d[1]-e[1]/5,zb,yb+d[1]-e[1],zb+h],str(qpz) + "·(" + cpe_str[1] + cpi_str_inv[1] + ") = " + str(round(W_B[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"2 3","YZ",W_C[1],[yb+d[1]-e[1],zb,yb,zb+h],str(qpz) + "·(" + cpe_str[2] + cpi_str_inv[1] + ") = " + str(round(W_C[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"5","XZ",W_D[1],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[3] + cpi_str_inv[1] + ") = " + str(round(W_D[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"4","XZ",W_Ey[1],[xb,zb,xb+b[1],zb+h],str(qpz) + "·(" + cpe_str[4][1] + cpi_str_inv[1] + ") = " + str(round(W_Ey[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"1","XY",W_F[1],[xb,yb+d[1],xb+e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[5] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"1","XY",W_F[1],[xb+b[1],yb+d[1],xb+b[1]-e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[6] + cpi_str_inv[1] + ") = " + str(round(W_F[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"1","XY",W_G[1],[xb+e[1]/4,yb+d[1],xb+b[1]-e[1]/4,yb+d[1]-e[1]/10],str(qpz) + "·(" + cpe_str[7] + cpi_str_inv[1] + ") = " + str(round(W_G[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"1","XY",W_H[1],[xb,yb+d[1]-e[1]/10,xb+b[1],yb+d[1]-e[1]/2],str(qpz) + "·(" + cpe_str[8] + cpi_str_inv[1] + ") = " + str(round(W_H[1],2)) + " kN/m²")
    WindFreeRecLoad(414,"1","XY",W_Id,[xb,yb+d[1]-e[1]/2,xb+b[1],yb],str(qpz) + "·(" + cpe_str[9] + cpi_str_inv[1] + ") = " + str(round(W_Id,2)) + " kN/m²")



    Model.clientModel.service.finish_modification()

if __name__ == '__main__':
    Model(False, "MFE_HAL")
    Wind(1.11,20,15,6.5,0.5,0.2,1,Model)
    print(interpol(7.5,7,8,10,20))