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
from RFEM.BasicObjects.surface import Surface
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType

if __name__ == '__main__':
    Model(True, "MultipleTests_MFE") # Create new model called MultipleTests_MFE
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')
    Material(2, 'S275')
    Material(3, 'S355')

    Section(1,'IPE 200',3) # Profiel uitvoeren in S355
    Section(2,'IPE 300',1) # Profiel uitvoeren in S235

    aantal = 10 # The amount of elements to be created

    # 10 Elementen maken:
    for i in range(1,aantal+1):

        #Knoop aanmaken:
        Node(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_NODE),2*(i-1.0),0.0,0.0)

        #Lijn aanmaken en hier een member van maken:
        Node(aantal+6*(i-1)+1,2*(i-1.0),1.0,0.0)
        Node(aantal+6*(i-1)+2,2*(i-1.0)+1,1.0,0.0)

        Member.Beam(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER),aantal+6*(i-1)+1,aantal+6*(i-1)+2,start_section_no=2,end_section_no=2)

        Node(aantal+6*(i-1)+3,2*(i-1.0),2.0,0.0)
        Node(aantal+6*(i-1)+4,2*(i-1.0)+1.0,2.0,0.0)
        Node(aantal+6*(i-1)+5,2*(i-1.0)+1.0,3.0,0.0)
        Node(aantal+6*(i-1)+6,2*(i-1.0),3.0,0.0)
        SurfaceLines = str(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE)) + " "
        Line(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE),str(aantal+6*(i-1)+3)+" "+str(aantal+6*(i-1)+4))
        SurfaceLines += str(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE)) + " "
        Line(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE),str(aantal+6*(i-1)+4)+" "+str(aantal+6*(i-1)+5))
        SurfaceLines += str(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE)) + " "
        Line(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE),str(aantal+6*(i-1)+5)+" "+str(aantal+6*(i-1)+6))
        SurfaceLines += str(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE)) + " "
        Line(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_LINE),str(aantal+6*(i-1)+6)+" "+str(aantal+6*(i-1)+3))
        Surface(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_SURFACE),SurfaceLines)

    Model.clientModel.service.finish_modification()
    nodes = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_NODE)
    for j in nodes:
        node1 = Node.GetNode(j)
        if node1.coordinate_1 == 14:
            print(node1['no'], str(node1.coordinate_1))



