from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.thickness import Thickness
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.surface import Surface
from RFEM.BasicObjects.opening import Opening
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Loads.lineLoad import LineLoad
from RFEM.Loads.nodalLoad import NodalLoad
from RFEM.Loads.surfaceLoad import SurfaceLoad
from RFEM.Loads.freeLoad import FreeLoad
from RFEM.Loads.imposedNodalDeformation import ImposedNodalDeformation
from RFEM.Loads.openingLoad import OpeningLoad
from RFEM.TypesForLines.lineSupport import LineSupport
from RFEM.Loads.imposedLineDeformation import ImposedLineDeformation
if Model.clientModel is None:
    Model()

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad(1, 1, '1', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 5000)

    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.no == 1
    assert nodal_load.force_magnitude == 5000