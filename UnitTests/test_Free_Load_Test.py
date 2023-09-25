import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RFEM.Loads.freeLoad import FreeLoad
from math import pi
from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.thickness import Thickness
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.surface import Surface
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase

if Model.clientModel is None:
    Model()

def test_free_load():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, 10.0, 0.0, 0.0)
    Node(3, 10.0, 10.0, 0.0)
    Node(4, 0.0, 10.0, 0.0)
    Node(5, 0.0, 0.0, 10.0)
    Node(6, 0.0, 10.0, 10.0)

    Line(1, '1 2')
    Line(2, '2 3')
    Line(3, '3 4')
    Line(4, '4 1')

    Thickness(1, 'Dicke', 1, 0.05)
    Surface(1, '1-4', 1)

    NodalSupport(1, '1', NodalSupportType.HINGED)
    NodalSupport(2, '2', NodalSupportType.HINGED)
    NodalSupport(3, '3', NodalSupportType.HINGED)
    NodalSupport(4, '4', NodalSupportType.HINGED)

    StaticAnalysisSettings(1, 'Geometrisch-linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)

    LoadCase(1 , 'Einzell- u. Linienlast')
    LoadCase(2 , 'Rechtecklast 1')
    LoadCase(3 , 'Rechtecklast 2')
    LoadCase(4 , 'Kreislast')
    LoadCase(5 , 'Polygonlast')

    # Prüfung der freien Einzellasten
    FreeLoad.ConcentratedLoad(1, 1, load_parameter= [5000, 4, 2])
    FreeLoad.ConcentratedLoad(2, 1, load_parameter= [50, 8, 9], load_type= FreeConcentratedLoadLoadType.LOAD_TYPE_MOMENT, load_direction= FreeConcentratedLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Y)

    # Prüfung der freien Linienlasten
    FreeLoad.LineLoad(3, 1, '1',
                        FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                        FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                        FreeLineLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                        [5000, 2, 3, 4, 5])

    # Prüfung der freien Rechtecklasten

    ##  LOAD_LOCATION_RECTANGLE_CORNER_POINTS
    FreeLoad.RectangularLoad(1, 2, '1',
                             FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [5000],
                             FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                             [1, 8, 3, 10, 0])

    FreeLoad.RectangularLoad(2, 2, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000, 2000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                            [4, 8, 6, 10, 0])

    FreeLoad.RectangularLoad(3, 2, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000, 2000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                            [7, 8, 9, 10, 0])

    FreeLoad.RectangularLoad(4, 2, '1',
                             FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [5000],
                             FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                             [1, 5, 3, 7, [[-3, 0.3], [-1, 0.4], [0, 1]]])

    FreeLoad.RectangularLoad(5, 2, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                            [4, 5, 6, 7, [5, 7, 0], [5, 9, 2], 0, [[0, 0.5], [90, 1.75], [180, 1.25], [270, 1], [360, 0.5]]])

    FreeLoad.RectangularLoad(6, 2, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                            [7, 5, 9, 7, [[-3, 0.3], [-1, 0.4], [0, 1]], [5, 7, 0], [5, 9, 2], 0, [[0, 0.5], [90, 1.75], [180, 1.25], [270, 1], [360, 0.5]]])

    ##  LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES
    FreeLoad.RectangularLoad(1, 3, '1',
                             FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [5000],
                             FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                             [2, 9, 2, 2, 10])

    FreeLoad.RectangularLoad(2, 3, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000, 2000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                            [5, 9, 2, 2, 0])

    FreeLoad.RectangularLoad(3, 3, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000, 2000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                            [8, 9, 2, 2, 0])

    FreeLoad.RectangularLoad(4, 3, '1',
                             FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [5000],
                             FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                             [2, 6, 2, 2, [[-3, 0.3], [-1, 0.4], [0, 1]]])

    FreeLoad.RectangularLoad(5, 3, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                            [5, 6, 2, 3, [5, 7, 0], [5, 9, 2], 0, [[0, 0.5], [90, 1.75], [180, 1.25], [270, 1], [360, 0.5]]])

    FreeLoad.RectangularLoad(6, 3, '1',
                            FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER,
                            FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                            FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                            [5000],
                            FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES,
                            [8, 6, 2, 2, [[-3, 0.3], [-1, 0.4], [0, 1]], [5, 7, 0], [5, 9, 2], 0, [[0, 0.5], [90, 1.75], [180, 1.25], [270, 1], [360, 0.5]]])

    # Prüfung der freien Kreislasten
    FreeLoad.CircularLoad(1, 4, '1',
                             FreeCircularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeCircularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [10000, 7.5, 5, 2])

    FreeLoad.CircularLoad(2, 4, '1',
                             FreeCircularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR,
                             FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                             FreeCircularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                             [10000, 2500, 2.5, 5, 2])

    # Prüfung der freien Polygonlasten
    FreeLoad.PolygonLoad(1, 5, '1',
                         FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                         FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         FreePolygonLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                         [[1, 0], [0, 2], [2, 2]],
                         [5000])

    FreeLoad.PolygonLoad(2, 5, '1',
                         FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR,
                         FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         FreePolygonLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                         [[6, 0], [4, 2], [8, 2]],
                         [5000, 2500, 1000, 1, 2, 3])

    FreeLoad.PolygonLoad(3, 5, '1',
                         FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST,
                         FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         FreePolygonLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                         [[6, 4], [4, 6], [8, 6]],
                         [5000, 2500, 1, 3])

    FreeLoad.PolygonLoad(4, 5, '1',
                         FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND,
                         FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                         FreePolygonLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                         [[1, 4], [0, 6], [2, 6]],
                         [1500, 7500, 2, 1])

    Model.clientModel.service.finish_modification()

    fcl = Model.clientModel.service.get_free_concentrated_load(2, 1)
    assert fcl.load_type == 'LOAD_TYPE_MOMENT'
    assert fcl.magnitude == 50.0
    assert fcl.load_location_x == 8
    assert fcl.load_location_y == 9

    fll = Model.clientModel.service.get_free_line_load(3, 1)
    assert fll.load_projection == 'LOAD_PROJECTION_XY_OR_UV'
    assert fll.load_direction == 'LOAD_DIRECTION_GLOBAL_Z_TRUE'
    assert fll.magnitude_uniform == 5000
    assert fll.load_location_first_y == 3
    assert fll.load_location_second_y == 5

    frl = Model.clientModel.service.get_free_rectangular_load(5, 3)
    fr2 = Model.clientModel.service.get_free_rectangular_load(1, 3)
    assert frl.load_projection == 'LOAD_PROJECTION_XY_OR_UV'
    assert frl.load_direction == 'LOAD_DIRECTION_GLOBAL_Z_TRUE'
    assert frl.load_distribution == 'LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER'
    assert frl.load_location_center_y == 6
    assert frl.load_location_center_side_b == 3
    assert fr2.load_location_rotation == 10 * (pi/180)

    fcl = Model.clientModel.service.get_free_circular_load(2, 4)
    assert fcl.magnitude_center == 10000
    assert fcl.magnitude_radius == 2500
    assert fcl.load_location_y == 5
    assert fcl.load_location_radius == 2

    fpl = Model.clientModel.service.get_free_polygon_load(4, 5)
    assert fpl.magnitude_linear_2 == 7500
    assert fpl.magnitude_linear_location_1 == 2
    assert fpl.load_location[0][0].row.second_coordinate == 4
    assert fpl.load_location[0][2].row.first_coordinate == 2
