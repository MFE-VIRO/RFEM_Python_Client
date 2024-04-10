import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

# from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
# from RFEM.BasicObjects.member import Member

if __name__ == '__main__':
    Model(False, "") #Work in current RFEM6 model
    Model.clientModel.service.begin_modification()

#Change material properties
    material = Model.clientModel.service.get_material(1)
    material.name='S355'
    material.comment='OPMERKING'
    material.no=1
    Model.clientModel.service.set_material(material)

#Change section properties
    section = Model.clientModel.service.get_section(2)
    section.name='IPE 300'
    section.comment='OPMERKING'
    section.material=1
    section.no=2
    section.rotation_angle=0.0
    section.warping_stiffness_deactivated=True
    Model.clientModel.service.set_section(section)

# ToDo: Change thicknesses

#Change node properties
    node = Model.clientModel.service.get_node(2)
    node.global_coordinate_1=3
    node.global_coordinate_2=3
    node.global_coordinate_3=3
    node.no=2
    node.comment='OPMERKING'
    node.support=0
    Model.clientModel.service.set_node(node)

# Change line properties
    line = Model.clientModel.service.get_line(1)
    line.comment='OPMERKING'
    line.definition_nodes='1 2'
    line.member=1
    line.no=1
    line.support=0
    Model.clientModel.service.set_line(line)


    node = Model.clientModel.service.get_node(2)
    node.global_coordinate_1=3
    Model.clientModel.service.set_node(node)

    Model.clientModel.service.finish_modification()


