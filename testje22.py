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

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Force(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [6000])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 6000