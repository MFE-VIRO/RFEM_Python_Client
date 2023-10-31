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
    FreeLoad.PolygonLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_POLYGON_LOAD,model=model),load_case_no=401,surfaces_no=1)

    BaseNode = Node.GetNode(BaseNodeNo,model)
    Model.clientModel.service.finish_modification()

if __name__ == '__main__':
    Model(False, "MFE_HAL")
    Wind(20,15,6.5,0.5,1,Model)