#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

# Import the relevant Libraries
from RFEM.enums import SurfaceLoadDistributionDirection
from RFEM.initModel import Model
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.thickness import Thickness
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.surface import Surface

if Model.clientModel is None:
    Model()

def test_load_distribution_surface():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    # Testing the Default Function
    Node(1, 0, -30, 0), Node(2, 10, -30, 0), Node(3, 10, -20, 0), Node(4, 0, -20, 0)
    Line(1, '1 2'), Line(2, '2 3'), Line(3, '3 4'), Line(4, '4 1')
    Material(name='C30/37')
    Thickness()
    Surface(params={'grid_enabled':True})

    # Standard Even Load Distribution
    Node(5, 0, -15, 0), Node(6, 10, -15, 0), Node(7, 10, -5, 0), Node(8, 0, -5, 0)
    Line(5, '5 6'), Line(6, '6 7'), Line(7, '7 8'), Line(8, '8 5')
    Surface.LoadDistribution(2, '5 6 7 8', SurfaceLoadDistributionDirection.LOAD_TRANSFER_DIRECTION_IN_BOTH,
                         True, 10, loaded_lines='6 7 8', excluded_lines='5')

    Model.clientModel.service.finish_modification()

    surface = Model.clientModel.service.get_surface(2)
    assert surface.no == 2
    assert surface.geometry == "GEOMETRY_PLANE"
    assert surface.type == "TYPE_LOAD_TRANSFER"
    assert surface.boundary_lines == "5 6 7 8"
    assert surface.analytical_area == 100.0
    assert surface.analytical_center_of_gravity_x == 5.0
    assert surface.analytical_center_of_gravity_y == -10.0
    assert surface.analytical_center_of_gravity_z == 0.0
    assert surface.area == 100.0
    assert surface.center_of_gravity_x == 5.0
    assert surface.center_of_gravity_y == -10.0
    assert surface.center_of_gravity_z == 0.0
    assert surface.position == "In plane XY of global CS"
    assert surface.position_short == "In XY"
    assert surface.load_transfer_direction == "LOAD_TRANSFER_DIRECTION_IN_BOTH"
    assert surface.is_surface_weight_enabled == True
    assert surface.is_advanced_distribution_settings_enabled == False
    assert surface.surface_weight == 10.0
    assert surface.consider_member_eccentricity == False
    assert surface.consider_section_distribution == False
    assert surface.load_distribution == "LOAD_DISTRIBUTION_VARYING"
    assert surface.neglect_equilibrium_of_moments == False
    assert surface.excluded_lines == '5'
