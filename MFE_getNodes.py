
from RFEM.enums import ObjectTypes
from RFEM.initModel import Model
from RFEM.BasicObjects.node import Node
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType

def getNodes(model = Model):
    NodeNumbers = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_NODE,model)
    nodes = []
    for n in NodeNumbers:
        node = Node.GetNode(n,model)
        nodes.append({"No":node.no,"X": node.coordinate_1, "Y": node.coordinate_2, "Z": node.coordinate_3})
    return nodes
