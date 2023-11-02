from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, ConvertToDlString, SetAddonStatus, FirstFreeIdNumber, insertSpaces
from RFEM.BasicObjects.node import Node

from RFEM.LoadCasesAndCombinations.loadCase import LoadCase

from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Loads.freeLoad import FreeLoad
from RFEM.Calculate.meshSettings import GetModelInfo
# from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf

def Wind(
        Lx : float = 10,
        Ly : float = 20,
        h : float = 5,
        h_dr : float = 0.5,
        BaseNodeNo : int = 1,
        model = Model
        ):
    b=[Ly,Lx]
    d=[Lx,Ly]
    e=[min(b[0],2*h),min(b[1],2*h)]


#TIJDELIJKE INVOER VOOR TESTEN. DIT MOETEN UITEINDELIJK FORMULES WORDEN MET Cpe, Cpi en qpw.
    W_F = [-2.0,-3.0]
    W_G = [-1.5,-2.0]
    W_H = [-1.0,-1.5]
    W_Id = [0.5,0.7]
    W_Iz = [-0.5,-0.7]


    Model.clientModel.service.begin_modification()

    BaseNode = Node.GetNode(BaseNodeNo,model)
    xb = BaseNode.coordinate_1
    yb = BaseNode.coordinate_2
    zb = BaseNode.coordinate_3

    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,401),
                         load_case_no=401,surfaces_no="1",
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location=[[xb,yb],[xb+e[0]/10,yb],[xb+e[0]/10,yb+e[0]/4],[xb,yb+e[0]/4]],
                         params={'magnitude_uniform': W_F[0]*1000})

    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,401),
                         load_case_no=401,surfaces_no="1",
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location=[[xb,yb+b[0]],[xb+e[0]/10,yb+b[0]],[xb+e[0]/10,yb+b[0]-e[0]/4],[xb,yb+b[0]-e[0]/4]],
                         params={'magnitude_uniform': W_F[0]*1000})

    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,401),
                         load_case_no=401,surfaces_no="1",
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location=[[xb,yb+e[0]/4],[xb+e[0]/10,yb+e[0]/4],[xb+e[0]/10,yb+b[0]-e[0]/4],[xb,yb+b[0]-e[0]/4]],
                         params={'magnitude_uniform': W_G[0]*1000})

    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,401),
                         load_case_no=401,surfaces_no="1",
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location=[[xb+e[0]/10,yb],[xb+e[0]/2,yb],[xb+e[0]/2,yb+b[0]],[xb+e[0]/10,yb+b[0]]],
                         params={'magnitude_uniform': W_H[0]*1000})

    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,401),
                         load_case_no=401,surfaces_no="1",
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location=[[xb+e[0]/2,yb],[xb+d[0],yb],[xb+d[0],yb+b[0]],[xb+e[0]/2,yb+b[0]]],
                         params={'magnitude_uniform': W_Iz[0]*1000})


    Model.clientModel.service.finish_modification()

if __name__ == '__main__':
    Model(False, "MFE_HAL")
    Wind(20,15,6.5,0.5,1,Model)