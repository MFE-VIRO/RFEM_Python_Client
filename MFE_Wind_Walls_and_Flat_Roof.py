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

    Model.clientModel.service.begin_modification()

    BaseNode = Node.GetNode(BaseNodeNo,model)
    xb = BaseNode.coordinate_1
    yb = BaseNode.coordinate_2
    zb = BaseNode.coordinate_3
    # FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,0,model),
    #                      load_case_no=401,surfaces_no=1,
    #                      load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
    #                      load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
    #                      load_location={'free_polygon_load_load_location': [{'no': 1,'row': {'first_coordinate': xb, 'second_coordinate': yb+b[0],}},
    #                      {'no': 2, 'row': {'first_coordinate': xb+3, 'second_coordinate': yb+b[0]}},
    #                      {'no': 3, 'row': {'first_coordinate': xb+3, 'second_coordinate': yb+b[0]-6}},
    #                      {'no': 4, 'row': {'first_coordinate': xb, 'second_coordinate': yb+b[0]-6}}]},params={'magnitude_uniform': -5000.0})

    FreeLoad.PolygonLoad(0,
                         load_case_no=401,surfaces_no=1,
                         load_projection=FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         load_direction=FreePolygonLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                         load_location={'free_polygon_load_load_location': [{'no': 1,'row': {'first_coordinate': xb, 'second_coordinate': yb+b[0],}},
                         {'no': 2, 'row': {'first_coordinate': xb+3, 'second_coordinate': yb+b[0]}},
                         {'no': 3, 'row': {'first_coordinate': xb+3, 'second_coordinate': yb+b[0]-6}},
                         {'no': 4, 'row': {'first_coordinate': xb, 'second_coordinate': yb+b[0]-6}}]},params={'magnitude_uniform': -5000.0})

    Model.clientModel.service.finish_modification()

if __name__ == '__main__':
    Model(False, "MFE_HAL")
    Wind(20,15,6.5,0.5,1,Model)