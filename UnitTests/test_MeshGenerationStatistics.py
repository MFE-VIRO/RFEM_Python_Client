import sys
sys.path.append(".")
import pytest
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.BasicObjects.surface import Surface
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.thickness import Thickness 
from RFEM.BasicObjects.material import Material
from RFEM.initModel import *
from RFEM.enums import *

def test_generation_mesh_implemented():

    exist = method_exists(clientModel,'generate_mesh')
    assert exist == False #test fail once method is in T9 master or GM

@pytest.mark.skip("all tests still WIP")
def test_generation_of_mesh_statistics():
    # modal analysis not yet implemmented in released RFEM6
    clientModel.service.begin_modification()

    # Create Material
    Material(1, 'S235')
    Thickness(1, '20 mm', 1, 0.02)

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 0, 5, 0)
    Node(4, 5, 5, 0)

    Line(1, '1 2')
    Line(2, '2 4')
    Line(3, '4 3')
    Line(4, '3 1')

    Surface(1, '1 2 3 4', 1)

    NodalSupport(1, '1 2 3 4', NodalSupportType.FIXED)

    GenerateMesh()

    print('Ready!')

    clientModel.service.finish_modification()

    mesh_stats = GetMeshStatics()

    print(mesh_stats)
