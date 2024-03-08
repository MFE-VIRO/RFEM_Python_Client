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

from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.designSituation import clearAttributes, DesignSituation
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.LoadCasesAndCombinations.loadCombination import LoadCombination
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.dataTypes import inf

if __name__ == '__main__':
    Model(False, "NewTemplate_IMP")
    Model.clientModel.service.begin_modification()
#----------------------------------------------------------------------------------------------
#
#                       BELASTINGEN
#
#----------------------------------------------------------------------------------------------
    sys.stdout.write("\r                                                                       ")
    sys.stdout.write("\rBELASTINGEN\n")
    sys.stdout.flush()

    # LoadCasesAndCombinations({
    #                 "current_standard_for_combination_wizard": 6047,
    #                 "activate_combination_wizard_and_classification": True,
    #                 "activate_combination_wizard": True,
    #                 "result_combinations_active": False,
    #                 "result_combinations_parentheses_active": False,
    #                 "result_combinations_consider_sub_results": False,
    #                 "combination_name_according_to_action_category": False},
    #              model= Model)

    # LoadCase.StaticAnalysis(10, 'PB: Eigen Gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[True, 0.0, 0.0, -1.0])
    # LoadCase.StaticAnalysis(20, 'PB: Vloerafwerking en dakbedekking',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(30, 'PB: Gevelbekleding',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(40, 'PB: Trappen, leuningen en bordessen',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(50, 'PB: Klein installatie werk (gelijkmatig verdeeld)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(60, 'PB: Grote leidingen en leidingsupports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(70, 'PB: Overige supports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    # LoadCase.StaticAnalysis(80, 'PB: Gronddrukken',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    # LoadCase.StaticAnalysis(90, 'PB: Reserve',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(100, 'VB: Opgelegde belasting op vloeren (momentaan)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(300, 'VB: Sneeuw en/of aanvriezing',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_SNOW_ICE_LOADS_H_LESS_OR_EQUAL_TO_1000_M_QS, self_weight=[False])
    LoadCase.StaticAnalysis(401, 'VB: Wind (+X richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(402, 'VB: Wind (-X richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(403, 'VB: Wind (+Y richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(404, 'VB: Wind (-Y richting; overdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(411, 'VB: Wind (+X richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(412, 'VB: Wind (-X richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(413, 'VB: Wind (+Y richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(414, 'VB: Wind (-Y richting; onderdruk)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(510, 'VB: Thermische belasting (geval 1)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_TEMPERATURE_NON_FIRE_QT, self_weight=[False])
    LoadCase.StaticAnalysis(520, 'VB: Thermische belasting (geval 2)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_TEMPERATURE_NON_FIRE_QT, self_weight=[False])
    LoadCase.StaticAnalysis(611, 'Hijslasten (geval 1 met hor. kracht in +X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(612, 'Hijslasten (geval 1 met hor. kracht in -X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(613, 'Hijslasten (geval 1 met hor. kracht in +Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(614, 'Hijslasten (geval 1 met hor. kracht in -Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(710, 'BB: Stootbelastingen of ontploffingen (geval 1)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_ACCIDENTAL_ACTIONS_A, self_weight=[False])
    LoadCase.StaticAnalysis(720, 'BB: Stootbelastingen of ontploffingen (geval 2)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_ACCIDENTAL_ACTIONS_A, self_weight=[False])
    LoadCase.StaticAnalysis(900, 'PB: Equipement - lege gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(910, 'PB: Equipement - operationele gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    LoadCase.StaticAnalysis(920, 'PB: Equipement - test gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    LoadCase.StaticAnalysis(990, 'Voorspanning trekschoren',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PRESTRESS_P, self_weight=[False])

# COMBINATIONWIZARD:
w = CombinationWizard(1,consider_imperfection_case=False, params={'consider_initial_state': False,'structure_modification_enabled': False})
DesignSituation(1,DesignSituationType.DESIGN_SITUATION_TYPE_STR_PERMANENT_AND_TRANSIENT_6_10A_6_10B,True,'ULS (STR/GEO) - Permanent and transient - Eq. 6.10a and 6.10b',params={'combination_wizard': 1})
DesignSituation(2,DesignSituationType.DESIGN_SITUATION_TYPE_SLS_CHARACTERISTIC,True,'SLS - Characteristic',params={'combination_wizard': 1})

Model.clientModel.service.finish_modification()