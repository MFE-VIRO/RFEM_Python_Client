import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from RFEM.enums import *
from RFEM.initModel import *
from RFEM.LoadCasesAndCombinations import loadCase
from RFEM.Loads import membersetload

from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.LoadCasesAndCombinations.designSituation import clearAttributes, DesignSituation
from RFEM.LoadCasesAndCombinations.loadCase import LoadCase, ActionCategoryType
from RFEM.LoadCasesAndCombinations.loadCombination import LoadCombination
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType
from RFEM.dataTypes import inf

MemberSetNr = 38
StartRel = 0.01
EindRel =  0.99
Stap =     0.02
LoadCase1 = 900

Fv = 11500 #N
Fh = 1150  #N
eh = 0.20  #m

if __name__ == '__main__':
    Model(False, "") #Work in current RFEM6 model
    Model.clientModel.service.begin_modification()

    # LC_numbers = GetObjectNumbersByType(ObjectType=ObjectTypes.E_OBJECT_TYPE_LOAD_CASE)
    # for LC_number in LC_numbers:
    #     if
    #     Model.clientModel.service.delete_object(ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name, LC_number)

#----------------------------------------------------------------------------------------------
#                       STATIC ANALYSIS SETTINGS
#----------------------------------------------------------------------------------------------
    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")



    xRel = StartRel
    LC_number = LoadCase1
    i = 1
    while xRel<=EindRel:
        loadCase.LoadCase(LC_number,"VB: Hijslast " + str(i),action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
        membersetload.MemberSetLoad.Force(1,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_Z,[True, Fv, xRel],'')

        LC_number = LC_number+1
        xRel = xRel + Stap
        i=i+1

    xRel = StartRel
    i = 1
    while xRel<=EindRel:
        loadCase.LoadCase(LC_number,"VB: Hijslast " + str(i),action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
        membersetload.MemberSetLoad.Force(1,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_Z,[True, Fv, xRel],'')
        membersetload.MemberSetLoad.Force(2,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_Y,[True, Fh, xRel],'')
        membersetload.MemberSetLoad.Moment(3,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_X,[True,-Fh*eh,xRel],'')
        LC_number = LC_number+1
        xRel = xRel + Stap
        i=i+1

    xRel = StartRel
    i = 1
    while xRel<=EindRel:
        loadCase.LoadCase(LC_number,"VB: Hijslast " + str(i),action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
        membersetload.MemberSetLoad.Force(1,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_Z,[True, Fv, xRel],'')
        membersetload.MemberSetLoad.Force(2,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_Y,[True, -Fh, xRel],'')
        membersetload.MemberSetLoad.Moment(3,LC_number,str(MemberSetNr),MemberSetLoadDistribution.LOAD_DISTRIBUTION_CONCENTRATED_1, MemberSetLoadDirection.LOAD_DIRECTION_LOCAL_X,[True,Fh*eh,xRel],'')

        LC_number = LC_number+1
        xRel = xRel + Stap
        i=i+1

Model.clientModel.service.finish_modification()