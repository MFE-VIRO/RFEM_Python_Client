from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all
from RFEM.baseSettings import BaseSettings
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
from RFEM.dataTypes import inf
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue
from RFEM.Results.designOverview import GetDesignOverview, GetPartialDesignOverview

import math

if __name__ == '__main__':
    Model(True, "ExampleMIFbySection.rf6")
    # Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()
    BaseSettings(9.81, GlobalAxesOrientationType.E_GLOBAL_AXES_ORIENTATION_ZUP, LocalAxesOrientationType.E_LOCAL_AXES_ORIENTATION_ZDOWN)

    Material(1, 'S235JR | EN 10025-2:2019-08')

    Section(11, 'IPE 200 | Euronorm 19-57; ... | SZS', 1)
    Section(12, 'IPE 240 | Euronorm 19-57; ... | SZS', 1)

    Node(1, 0.3, 0.0, 0.0)
    Node(2, 3.1, 0.0, 0.0)
    Node(3, 0.1, 2.0, 0.0)
    Node(4, 3.5, 2.0, 0.0)
    Node(5, 0.9, 4.0, 0.0)
    Node(6, 4.2, 4.0, 0.0)

    Member(21, 1, 2, 0, 11, 11)
    Member(22, 3, 4, 0, 12, 12)
    Member(23, 5, 6, 0, 12, 12)

    NodalSupport(1, '1 3 5', [inf, inf, inf, inf, 0.0, 0.0])
    NodalSupport(2, '2 4 6', [0.0, inf, inf, inf, 0.0, 0.0])

    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")

    LoadCasesAndCombinations({
                    "current_standard_for_combination_wizard": 6047,
                    "activate_combination_wizard_and_classification": True,
                    "activate_combination_wizard": True,
                    "result_combinations_active": False,
                    "result_combinations_parentheses_active": False,
                    "result_combinations_consider_sub_results": False,
                    "combination_name_according_to_action_category": False},
                 model= Model)

    LoadCase.StaticAnalysis(10, 'DL: Self-weight',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[True, 0.0, 0.0, -1.0])
    LoadCase.StaticAnalysis(20, 'DL: Other dead loads',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(100, 'LL: Imposed loads',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_B_OFFICE_AREAS_QI_B, self_weight=[False])

    CombinationWizard(31,consider_imperfection_case=False, params={'consider_initial_state': False,'structure_modification_enabled': False})
    DesignSituation(41,DesignSituationType.DESIGN_SITUATION_TYPE_STR_PERMANENT_AND_TRANSIENT_6_10A_6_10B,
                    True,'ULS (STR/GEO) - Permanent and transient - Eq. 6.10a and 6.10b',
                    params={'combination_wizard': 31})

    MemberLoad(1,20,"21",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-5000)
    MemberLoad(2,20,"22",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-5000)
    MemberLoad(3,20,"23",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-5000)
    MemberLoad(1,100,"21",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-15000)
    MemberLoad(2,100,"22",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-15000)
    MemberLoad(3,100,"23",MemberLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,-15000)


    Model.clientModel.service.finish_modification()

    Calculate_all()

    # I want to know the governing member internal forces in members with cross-section 12 (IPE 240; members 22 and 23)
    # for ULS DesignSituation (no 41):

    MIFS = ResultTables.MembersInternalForcesBySection(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,41,12,False)

    # When printing MIFS, I get the following list:
    # {'node_number': 1.0, 'internal_force_vz': 10279.0302734375, 'internal_force_n': 0.0, 'location': 0.0,
    # 'internal_force_mz': 0.0, 'internal_force_label': 'M<sub>z</sub>', 'member_number': 21.0, 'location_flags': 'L | M',
    # 'internal_force_my': 0.0, 'specification': 'CO13', 'internal_force_vy': 0.0, 'internal_force_mt': 0.0}]
    print(MIFS)


