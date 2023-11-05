import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from RFEM.enums import *
from RFEM.initModel import Model, Calculate_all, CalculateSelectedCases, ConvertToDlString, SetAddonStatus, FirstFreeIdNumber, insertSpaces
from RFEM.baseSettings import BaseSettings
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.memberSet import MemberSet
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.designSituation import clearAttributes, DesignSituation
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase
from RFEM.LoadCasesAndCombinations.loadCombination import LoadCombination
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.dataTypes import inf
from RFEM.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations
from RFEM.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations
from RFEM.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths

import math

EffLengthMembers = [[],[],[],[],[]]
EffLengthSets = [[],[],[],[],[]]
DesignPropsViaParentSet = bool

if __name__ == '__main__':
    Model()

    Model.clientModel.service.begin_modification()
    BaseSettings(9.81, GlobalAxesOrientationType.E_GLOBAL_AXES_ORIENTATION_ZUP, LocalAxesOrientationType.E_LOCAL_AXES_ORIENTATION_ZDOWN)
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)
    Model.clientModel.service.delete_all()
    Model.clientModel.service.finish_modification(); Model.clientModel.service.begin_modification()
    # Model.clientModel.service.begin_modification()

    #Instellingen Steel Effective Lengths voor kolommen maken:
    NodalSupportsList = []
    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0,
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0,
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES,
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO,
                                ""])
    for i in range(2): #TODO: Range afhankelijk maken van ny voor het geval de kolommen meer kniksteunen hebben.
        NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_INDIVIDUALLY, True, 0.0,
                                    SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0,
                                    SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
                                    SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                    ""])

    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0,
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0,
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES,
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO,
                                ""])

    SteelEffectiveLengths(5,"","", True, True, False, True, True, False, 'SEL5', NodalSupportsList, [[6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],[55, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1],[6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],[6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1]], intermediate_nodes=True,
                          different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE)


    SteelDesignUltimateConfigurations(1, name="EC3 checks UGT")
    Model.clientModel.service.finish_modification()

