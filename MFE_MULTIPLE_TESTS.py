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
from RFEM.BasicObjects.line import Line, LineType
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType

if __name__ == '__main__':
    Model(True, "MultipleTests_MFE") # crete new model called Ligger_op_twee_steunpunten
    Model.clientModel.service.begin_modification()
    aantal = 10
# Nodes maken    
    for i in range(1,aantal+1):
        Node(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_NODE),2*(i-1.0),0.0,0.0)

        Node(aantal+2*(i-1)+1,2*(i-1.0),1.0,0.0)
        Node(aantal+2*(i-1)+2,2*(i-1.0)+1,1.0,0.0)
        Line(i,str(aantal+2*(i-1)+1)+" "+str(aantal+2*(i-1)+2))
        

            
    
    

    
    Model.clientModel.service.finish_modification()
    nodes = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_NODE)
    for j in nodes:
        node1 = Node.GetNode(j)
        if node1.coordinate_1 == 14:
            print(node1['no'], str(node1.coordinate_1))


 
