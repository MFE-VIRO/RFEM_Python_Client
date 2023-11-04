from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, ConvertToDlString, SetAddonStatus, FirstFreeIdNumber, insertSpaces
from RFEM.BasicObjects.node import Node
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Loads.freeLoad import FreeLoad
from RFEM.dataTypes import inf

from MFE_ALG import *

def SnowFreeRecLoad(LC:int = 1,
                    surfaces: str="1",
                    load: float=1.0,                # in kN/m2
                    points: list=[0.0,0.0,1.0,1.0], # coördintaten in meters
                    comment: str="",
                    model = Model):

    points.append(0)

    FreeLoad.RectangularLoad(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_FREE_RECTANGULAR_LOAD,LC),
                             LC,surfaces,FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_PROJECTED,
                             [load*1000],FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                             points,comment)


def Sneeuw(
        Lx : float = 10,
        Ly : float = 20,
        dhr : float = 0.2,
        BaseNodeNo : int = 1,
        model = Model
        ):

    Model.clientModel.service.begin_modification()

    BaseNode = Node.GetNode(BaseNodeNo,model)
    xb = BaseNode.coordinate_1
    yb = BaseNode.coordinate_2
    zb = BaseNode.coordinate_3

    SnowFreeRecLoad(300,"1",-0.56,[xb,yb,xb+Lx,yb+Ly])

    Model.clientModel.service.finish_modification()

if __name__ == '__main__':
    Model(False, "MFE_HAL")
    Sneeuw(20,15,0.2,1,Model)