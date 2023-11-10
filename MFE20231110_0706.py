from RFEM.enums import *
from RFEM.initModel import *
from RFEM.BasicObjects.node import *

Model(False,"MFE_HAL.rf6")
node = Node.GetNode(37)
Model.clientModel.service.begin_modification()
Model.clientModel.service.delete_all_results(True) # Hiermee worden alle resultaten en het mesh verwijderd, zodat je het model kan wijzigen.

# Node(80,0.0,-5.0,0.0)
# Node(37,15.0,0.0,0.1)
Node(25,10.0,0.0,1.0)
Model.clientModel.service.finish_modification()
# print(n.coordinate_1)
