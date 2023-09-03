import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, FirstFreeIdNumber
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf

if __name__ == '__main__':
    Model(True, "MultipleTests_MFE") # crete new model called Ligger_op_twee_steunpunten
    Model.clientModel.service.begin_modification()
    for i in range(1,6):
            Node(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_NODE),i,0.0,0.0)
    Model.clientModel.service.finish_modification()


 
