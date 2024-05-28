import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RFEM.initModel import Model, getPathToRunningRFEM
from RFEM.enums import CaseObjectType
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue

if Model.clientModel is None:
    Model()

def test_result_tables():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.run_script(os.path.join(getPathToRunningRFEM(),'scripts\\internal\\Demos\\Demo-004 Bus Station-Concrete Design.js'))
    Model.clientModel.service.calculate_all(False)

    assert Model.clientModel.service.has_any_results()

    # CO1
    assert not ResultTables.LinesSupportForces(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 1)
    assert ResultTables.LinesSupportForces(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 3)
    assert ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert ResultTables.MembersInternalForcesBySection(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert not ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 4)
    assert ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 1)

    #LC1
    assert ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1,1)
    assert ResultTables.NodesDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 20)
    assert ResultTables.NodesSupportForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 16)
    assert ResultTables.Summary(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1)
    assert ResultTables.SurfacesBasicInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 4)

    #LC2
    assert not ResultTables.SurfacesBasicStresses(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 5)
    assert ResultTables.SurfacesBasicStresses(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 4)
    assert ResultTables.SurfacesBasicTotalStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 1)
    assert ResultTables.SurfacesDesignInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 2)
    assert ResultTables.SurfacesElasticStressComponents(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 3)
    assert ResultTables.SurfacesEquivalentStressesBach(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 2, 1)

    #RC1
    assert ResultTables.SurfacesEquivalentStressesRankine(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 1)
    assert ResultTables.SurfacesEquivalentStressesTresca(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 2)
    assert ResultTables.SurfacesEquivalentStressesMises(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 3)
    assert ResultTables.SurfacesEquivalentTotalStrainsBach(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 4)
    assert ResultTables.SurfacesEquivalentTotalStrainsMises(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 1)
    assert ResultTables.SurfacesEquivalentTotalStrainsRankine(CaseObjectType.E_OBJECT_TYPE_RESULT_COMBINATION, 1, 2)

    # DS1
    assert ResultTables.SurfacesEquivalentTotalStrainsTresca(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 3)
    assert ResultTables.SurfacesGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 4)
    assert ResultTables.SurfacesLocalDeformations(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 1)
    assert ResultTables.SurfacesMaximumTotalStrains(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 2)
    assert ResultTables.SurfacesPrincipalInternalForces(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 3)
    assert ResultTables.SurfacesPrincipalStresses(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 4)

    table = ResultTables.SurfacesPrincipalTotalStrains(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION, 1, 1)
    assert table

    table1 = ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=False)
    table2 = ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=True)
    table3 = ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=1, include_base=True, without_extremes=True)

    assert len(table1) > len(table2)
    assert len(table2) > len(table3)

    table4 = ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=False)
    table5 = ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=True)
    table6 = ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=1, include_base=True, without_extremes=True)

    assert len(table4) > len(table5)
    assert len(table5) > len(table6)

    table7 = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=False)
    table8 = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=True)
    table9 = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=1, include_base=True, without_extremes=True)

    assert len(table7) > len(table8)
    assert len(table8) > len(table9)

    table10 = ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=False)
    table11 = ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=0, include_base=True, without_extremes=True)
    table12 = ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,1, object_no=1, include_base=True, without_extremes=True)

    assert len(table10) > len(table11)
    assert len(table11) > len(table12)
