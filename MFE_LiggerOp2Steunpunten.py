import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, SetAddonStatus, FirstFreeIdNumber
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.designSituation import clearAttributes, DesignSituation
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.LoadCasesAndCombinations.loadCombination import LoadCombination
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf
from RFEM.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations
from RFEM.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations
from RFEM.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue
from RFEM.Results.designOverview import GetDesignOverview, GetPartialDesignOverview

import xlwings as xw

dirname = os.path.join(os.getcwd(), os.path.dirname(__file__))
path = os.path.join(dirname,'MFE_TEST.xlsx')
wb = xw.Book(path)

Sheet = wb.sheets(1)

if __name__ == '__main__':
    l = float(input('Lengte van de ligger in m: '))
    q = float(input('Gelijkmatig verdeelde belasting in kN/m: '))
    kipst = int(input('Aantal kipsteunen: '))

    Model(True, "Ligger_op_twee_steunpunten") # create new model called Ligger_op_twee_steunpunten
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)

    Material(1, 'S235')

    Section(1, 'IPE 200')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, l, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    for i in range(0,kipst):
        Node.OnMember(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_NODE),1,NodeReferenceType.REFERENCE_TYPE_L, parameters = [True, (i+1)/(kipst+1)])

    NodalSupport(1, '1', [inf, inf, inf, inf, 0.0, 0.0])
    NodalSupport(2, '2', [0.0, inf, inf, inf, 0.0, 0.0])

    SteelEffectiveLengths(1, "1", "", False, False, False, True, True, False, 'SEL1',
        [
            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""]
        ],
        intermediate_nodes=True, different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE
                        )

    SteelDesignUltimateConfigurations(1, name="EC3 checks UGT")
    SteelDesignServiceabilityConfigurations(1,"EC3 checks BGT",)

    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")

    LoadCasesAndCombinations({
                    "current_standard_for_combination_wizard": 6047,
                    "activate_combination_wizard_and_classification": True,
                    "activate_combination_wizard": True,
                    "result_combinations_active": True,
                    "result_combinations_parentheses_active": True,
                    "result_combinations_consider_sub_results": True,
                    "combination_name_according_to_action_category": True
                 },
                 model= Model)

    LoadCase.StaticAnalysis(1, 'Self-Weight',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G,self_weight=[True, 0.0, 0.0, 1.0])
    LoadCase.StaticAnalysis(2, 'Variable',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_B_OFFICE_AREAS_QI_B)

    CombinationWizard(1, 'Wizard 1', 1, 1, False, False, 1, InitialStateDefintionType.DEFINITION_TYPE_FINAL_STATE, None, False, False, False, model = Model)

    DesignSituation(1,DesignSituationType.DESIGN_SITUATION_TYPE_STR_PERMANENT_AND_TRANSIENT_6_10A_6_10B, True, 'ULS (STR/GEO) - Permanent and transient - Eq. 6.10a and 6.10b', params = {'combination_wizard': 1})
    DesignSituation(2,DesignSituationType.DESIGN_SITUATION_TYPE_SLS_CHARACTERISTIC, params = {'combination_wizard': 1})

    MemberLoad.Force(1, 2, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, load_parameter=[1000])

    Model.clientModel.service.finish_modification()

    Sheet.clear_contents()
    Sheet["A1"].value = "CrossSection"
    Sheet["B1"].value = "Uz;max"
    Sheet["B2"].value = "[mm]"
    Sheet["C1"].value = "UCmax"
    Sheet["C2"].value = "[-]"

    row = 2
    #profielen = ["IPE 80", "IPE 100", "IPE 120", "IPE 140", "IPE 160", "IPE 180", "IPE 200", "IPE 220", "IPE 240", "IPE 270", "IPE 300", "IPE 330", "IPE 360", "IPE 400", "IPE 450", "IPE 500", "IPE 550", "IPE 600"]
    profielen = ["IPE 80"]

    for profiel in profielen:
        Model.clientModel.service.begin_modification()
        Section(1, profiel)
        Model.clientModel.service.finish_modification()
        Calculate_all()
        MIF = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,1,1)
        My_max = GetMaxValue(MIF,'internal_force_my')/1000
        GDeform = ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,2,1)
        Uz_max = GetMaxValue(GDeform,'displacement_z')*1000
        DO = GetDesignOverview()
        UCmax = round(DO[0][0].row['design_ratio'],3)

        row += 1
        Sheet["A" + str(row)].value = profiel
        Sheet["B" + str(row)].value = Uz_max
        Sheet["C" + str(row)].value = UCmax

        print(profiel + ": UCmax = " + str(UCmax))

    wait = input("Press Enter to continue.")

    wb.save(path)
    wb.app.quit()