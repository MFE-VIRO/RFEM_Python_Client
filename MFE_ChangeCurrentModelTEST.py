import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

# from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, SetAddonStatus, FirstFreeIdNumber
# from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
# from RFEM.BasicObjects.member import Member

if __name__ == '__main__':
    Model(False, "") # create new model called Ligger_op_twee_steunpunten
    Model.clientModel.service.begin_modification()
    section = Model.clientModel.service.get_section(1)
    section = Section(name='IPE 600')
    node = Model.clientModel.service.get_node(1)
    node = Node(coordinate_Z=1)

    Model.clientModel.service.finish_modification()


