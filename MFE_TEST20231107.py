import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

sys.stdout.write("\r                                                                       ")
sys.stdout.write("\rIMPORTEREN BIBLIOTHEKEN\n")
sys.stdout.flush()

# dict = {'A':'1','B':'2','C':'3','D':'4','E':'5','F':'6','G':'7','H':'8',\
#         'I':'9','J':'10','K':'11','L':'12','M':'13','N':'14','O':'15','P':'16',\
#         'Q':'17','R':'18','S':'19','T':'20','U':'21','V':'22','W':'23','X':'24',\
#         'Y':'25','Z':'26','AA':'27','AB':'28','AC':'29','AD':'30','AE':'31','AF':'32',\
#         'AG':'33','AH':'34','AI':'35','AJ':'36','AK':'37','AL':'38','AM':'39','AN':'40'}

import time
time1 = time.time()

from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, ConvertToDlString, SetAddonStatus, FirstFreeIdNumber, insertSpaces
from RFEM.baseSettings import BaseSettings
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.line import Line
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.memberSet import MemberSet
from RFEM.BasicObjects.surface import Surface
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.TypesForMembers.memberHinge import MemberHinge
# from RFEM.TypesForMembers.memberNonlinearity import MemberNonlinearity
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.designSituation import clearAttributes, DesignSituation
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.LoadCasesAndCombinations.loadCombination import LoadCombination
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.Loads.memberLoad import MemberLoad
from RFEM.Calculate.meshSettings import GetModelInfo
# from RFEM.ImportExport.exports import ExportDetailsOfDesignToCSV
from RFEM.dataTypes import inf
from RFEM.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations
from RFEM.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations
from RFEM.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue
from RFEM.Results.designOverview import GetDesignOverview, GetPartialDesignOverview

import MFE_ZoekNode
import MFE_getMembers
import MFE_getNodes
from MFE_Wind_Walls_and_Flat_Roof import Wind
from MFE_Sneeuw import Sneeuw

import math


if __name__ == '__main__':

    Model(True)
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

#----------------------------------------------------------------------------------------------
#
#                       STATIC ANALYSIS SETTINGS
#
#----------------------------------------------------------------------------------------------

    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")

#----------------------------------------------------------------------------------------------
#
#                       BELASTINGEN
#
#----------------------------------------------------------------------------------------------
    sys.stdout.write("\r                                                                       ")
    sys.stdout.write("\rBELASTINGEN\n")
    sys.stdout.flush()

    LoadCasesAndCombinations({
                    "current_standard_for_combination_wizard": 6047,
                    "activate_combination_wizard_and_classification": True,
                    "activate_combination_wizard": True,
                    "result_combinations_active": False,
                    "result_combinations_parentheses_active": False,
                    "result_combinations_consider_sub_results": False,
                    "combination_name_according_to_action_category": False},
                 model= Model)

    LoadCase.StaticAnalysis(10, 'PB: Eigen Gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[True, 0.0, 0.0, -1.0])
    # LoadCase.StaticAnalysis(20, 'PB: Vloerafwerking en dakbedekking',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(30, 'PB: Gevelbekleding',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(40, 'PB: Trappen, leuningen en bordessen',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(50, 'PB: Klein installatie werk (gelijkmatig verdeeld)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(60, 'PB: Grote leidingen en leidingsupports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(70, 'PB: Overige supports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(80, 'PB: Gronddrukken',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(90, 'PB: Reserve',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(100, 'VB: Opgelegde belasting op vloeren (momentaan)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(300, 'VB: Sneeuw en/of aanvriezing',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_SNOW_ICE_LOADS_H_LESS_OR_EQUAL_TO_1000_M_QS, self_weight=[False])
    LoadCase.StaticAnalysis(401, 'VB: Wind (+X richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(402, 'VB: Wind (-X richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(403, 'VB: Wind (+Y richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(404, 'VB: Wind (-Y richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(411, 'VB: Wind (+X richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(412, 'VB: Wind (-X richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(413, 'VB: Wind (+Y richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(414, 'VB: Wind (-Y richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    # LoadCase.StaticAnalysis(510, 'VB: Thermische belasting (geval 1)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_TEMPERATURE_NON_FIRE_QT, self_weight=[False])
    # LoadCase.StaticAnalysis(520, 'VB: Thermische belasting (geval 2)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_TEMPERATURE_NON_FIRE_QT, self_weight=[False])
    # LoadCase.StaticAnalysis(611, 'Hijslasten (geval 1 met hor. kracht in +X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    # LoadCase.StaticAnalysis(612, 'Hijslasten (geval 1 met hor. kracht in -X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    # LoadCase.StaticAnalysis(613, 'Hijslasten (geval 1 met hor. kracht in +Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    # LoadCase.StaticAnalysis(614, 'Hijslasten (geval 1 met hor. kracht in -Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    # LoadCase.StaticAnalysis(710, 'BB: Stootbelastingen of ontploffingen (geval 1)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_ACCIDENTAL_ACTIONS_A, self_weight=[False])
    # LoadCase.StaticAnalysis(720, 'BB: Stootbelastingen of ontploffingen (geval 2)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_ACCIDENTAL_ACTIONS_A, self_weight=[False])
    # LoadCase.StaticAnalysis(900, 'PB: Equipement - lege gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(910, 'PB: Equipement - operationele gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(920, 'PB: Equipement - test gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])


# COMBINATIONWIZARD:
w = CombinationWizard(1,consider_imperfection_case=False, params={'consider_initial_state': False,'structure_modification_enabled': False})
DesignSituation(1,DesignSituationType.DESIGN_SITUATION_TYPE_STR_PERMANENT_AND_TRANSIENT_6_10A_6_10B,True,'ULS (STR/GEO) - Permanent and transient - Eq. 6.10a and 6.10b',params={'combination_wizard': 1})
DesignSituation(2,DesignSituationType.DESIGN_SITUATION_TYPE_SLS_CHARACTERISTIC,True,'SLS - Characteristic',params={'combination_wizard': 1})

Model.clientModel.service.finish_modification()
