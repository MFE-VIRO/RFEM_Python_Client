import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, SetAddonStatus
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf
from RFEM.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations
from RFEM.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations
from RFEM.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths


if __name__ == '__main__':
    l = float(input('Lengte van de ligger in m: '))
    q = float(input('Gelijkmatig verdeelde belasting in kN/m: '))

    Model(True, "Ligger_op_twee_steunpunten") # crete new model called Ligger_op_twee_steunpunten
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)

    Material(1, 'S235')

    Section(1, 'IPE 200')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, l, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    NodalSupport(1, '1', [inf, inf, inf, inf, 0.0, 0.0])
    NodalSupport(2, '2', [0.0, inf, inf, inf, 0.0, 0.0])

    SteelEffectiveLengths(1, "1", "", True, True, True, True, True, True, 'SEL1',
        [
            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_INDIVIDUALLY, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_INDIVIDUALLY, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_INDIVIDUALLY, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""]
        ],
        intermediate_nodes=True, different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE
                        )

    SteelDesignUltimateConfigurations(1, name="EC3 checks UGT")
    SteelDesignServiceabilityConfigurations(1,"EC3 checks BGT","")


    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")

    LoadCase.StaticAnalysis(1, 'Self-Weight',analysis_settings_no=1,self_weight=[True, 0.0, 0.0, 1.0])
    LoadCase.StaticAnalysis(2, 'Variable',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_B_OFFICE_AREAS_QI_B)

    MemberLoad.Force(1, 2, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, load_parameter=[1000])

    Model.clientModel.service.finish_modification()

    # Calculate_all()
    messages = CalculateSelectedCases([1])
    if len(messages) != 0:
        print("Calculation finished unsuccessfully")
        print(messages)
        # for message in messages:
        #     print("{0}\t{1}: {2} - {3} {4} {5}".format("Yes" if message.result else "No", message.message_type.ToString(), message.message, message.@object, message.current_value, message.input_field))
    else:
        print("Calculation finished successfully")

    # model status
    modelStatus = GetModelInfo()
    print("Model is calculated" if modelStatus.property_has_results else "Model is not calculated")
    print("Model contains printout report" if modelStatus.property_has_printout_report else "Model has not printout report")
    print ("Model contains " +  str(modelStatus.property_node_count) + " nodes")
    print ("Model contains " +  str(modelStatus.property_line_count) + " lines")
    print ("Model contains " +  str(modelStatus.property_member_count) + " members")
    print ("Model contains " +  str(modelStatus.property_surface_count) + " surfaces")
    print ("Model contains " +  str(modelStatus.property_solid_count) + " solids")
    print ("Model contains " +  str(modelStatus.property_lc_count) + " load cases")
    print ("Model contains " +  str(modelStatus.property_co_count) + " load combinations")
    print ("Model contains " +  str(modelStatus.property_rc_count) + " result classes")
    print ("Model weight " +   str(modelStatus.property_weight))
    print ("Model dimension x " + str(modelStatus.property_dimensions.x))
    print ("Model dimension y " + str(modelStatus.property_dimensions.y))
    print ("Model dimension z " + str(modelStatus.property_dimensions.z))

    node = Model.clientModel.service.get_node(1)
    print ("Node x coordinate " + str(node.coordinate_1))
