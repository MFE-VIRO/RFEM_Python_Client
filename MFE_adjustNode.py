from RFEM.enums import *
from RFEM.initModel import *
from RFEM.BasicObjects.node import *

Model(False, "MFE_HAL.rf6")
# gsdfgd = Model.clientModel.factory.create('ns0:node value')

node = Node.GetNode(37)
node.coordinate_3 += 0.5
print(node.coordinate_3)

Model.clientModel.service.begin_modification()
Model.clientModel.service.delete_all_results(True) # Hiermee worden alle resultaten en het mesh verwijderd, zodat je het model kan wijzigen.

Node(node.no,node.coordinate_1,node.coordinate_2,node.coordinate_3,node.comment)
# Model.clientModel.service.set_node(node)
Model.clientModel.service.finish_modification()

