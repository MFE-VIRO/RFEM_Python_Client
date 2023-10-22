import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')
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
from RFEM.BasicObjects.member import Member
from RFEM.BasicObjects.memberSet import MemberSet
from RFEM.TypesForNodes.nodalSupport import NodalSupport
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
from RFEM.Results.designOverview import GetDesignOverview, GetPartialDesignOverview\

import MFE_ZoekNode
import MFE_getMembers
import MFE_getNodes

import math

print("T1 = " + str(time.time()-time1) + "s")

# print(ord("a"))
EffLengthMembers = [[],[],[],[]]
EffLengthSets = [[],[],[],[]]
DesignPropsViaParentSet = bool


def BeamLimitCharacteristic(value: int = 100, sls_no = 1):

    with open(dirName+r"./sls_char.js", "w") as std:

        std.write("STEEL_DESIGN.steel_design_sls_configurations[{}].settings_ec3.property_sl_beam_limit_characteristic = {}".format(sls_no, value))

    Model.clientModel.service.run_script(dirName+r"./sls_char.js")

    os.remove(dirName+r"./sls_char.js")

def SnowWizardMonopitch(nodeList: [1,2,3,4]):

    with open(dirName+r"./SnowWizard.js", "w") as snowwiz:

        snowwiz.write("var snowLoadWizard = new SnowLoadWizard();\n")
        snowwiz.write('snowLoadWizard.SetMonoPitchRoofType(undefined, [4, 9, 57, 52], load_cases[300])\n')

    Model.clientModel.service.run_script(dirName+r"./SnowWizard.js")\

    os.remove(dirName+r"./SnowWizard.js")

if __name__ == '__main__':
    dy = 5 #float(input("H.o.h. afstand tussen assen // x-as [m]: "))
    dx = 5 #float(input("H.o.h. afstand tussen assen // y-as [m]: "))
    nx = 5 #int(input("Aantal assen in x-richting: "))
    ny = 4 #int(input("Aantal assen in y-richting: "))
    h = 6.5 #float(input("Hoogte hal incl. dakrand [m]: "))
    h_dr = 0.5 #float(input("Hoogte dakrand [m]: "))
    kst_kol = 2 #int(input("Aantal kniksteunen van de kolommen: "))
    nodes_frame = 2*(3+kst_kol)+ny-2
    members_frame = 2*(2+kst_kol)+ny-1
    sup_nodes = []
    b = (ny-1)*dy

    nodes=[]

    Model(True, "MFE_HAL")
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()
    BaseSettings(9.81, GlobalAxesOrientationType.E_GLOBAL_AXES_ORIENTATION_ZUP, LocalAxesOrientationType.E_LOCAL_AXES_ORIENTATION_ZDOWN)

    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)

    Model.clientModel.service.finish_modification()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')
    Section(1, 'HEA 240', 1, "Profiel Kolommen 1")
    Section(2, 'HEA 200', 1, "Profiel Kolommen 2")
    Section(3, 'IPE 400', 1, "Profiel Hoofdliggers")
    Section(4, 'HEA 160', 1, "Profiel Dakliggers KOPSE GEVELS")
    Section(5, 'HEA 140', 1, "Profiel Dakliggers LANGSGEVELS")
    Section(6, 'HEA 120', 1, "Profiel Kipsteunen dak")
    Section(7, 'HEA 100', 1, "Profiel Horizontale gevelliggers KOPSE GEVELS")
    Section(8, 'HEA 100', 1, "Profiel Horizontale gevelliggers LANGSGEVELS")

    Section(9, 'HEA 100', 1, "Profiel Dakrand Verticaal")
    Section(10, 'HEA 100', 1, "Profiel Dakrand Horizontaal")

    for i in range(nx):
        n = i*nodes_frame
        m = i*members_frame

        #Model.clientModel.service.finish_modification(); Model.clientModel.service.begin_modification()

    #Kolommen op x-as maken
        Node(n+1, i*dx, 0.0, 0.0)
        sup_nodes.append(n+1)
        Members_in_Set = []

        if kst_kol==0:
            EffLengthMembers[1].append(m+kst_kol+1)
            DesignPropsViaParentSet = False
        else: DesignPropsViaParentSet = True

        if kst_kol >= 1:
            for k in range(kst_kol):
                Node(n+1+k+1, i*dx, 0.0, (k+1)*(h-h_dr)/(kst_kol+1))
                Member(m+k+1,n+k+1,n+1+k+1, math.radians(90) ,1,1,params={'design_properties_via_member': False, 'design_properties_via_parent_member_set': True})
                Members_in_Set.append(m+k+1)

                #Gevelligers op x-as
                if i>0:
                    EffLengthMembers[2].append(i+nx*members_frame+(ny-2+2)*(nx-1)+k*(nx-1))
                    Member(i+nx*members_frame+(ny-2+2)*(nx-1)+k*(nx-1),n+1+k+1-nodes_frame,n+1+k+1,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

        Node(n+kst_kol+2, i*dx, 0.0, h-h_dr)
        Member(m+kst_kol+1,n+kst_kol+1,n+kst_kol+2,math.radians(90),1,1,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})
        Members_in_Set.append(m+kst_kol+1)

        #Randbalk x-as maken
        if i>0:
            EffLengthMembers[2].append(i+nx*members_frame)
            Member(i+nx*members_frame,n-nodes_frame+kst_kol+2,n+kst_kol+2,math.radians(0),5,5,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

        if kst_kol >= 1:
            EffLengthSets[1].append(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET))
            MemberSet(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET), insertSpaces(Members_in_Set),SetType.SET_TYPE_CONTINUOUS,"Kolom",params={'design_properties_activated': True})


    #Kolommen op y = b maken

        Node(n+nodes_frame, i*dx, b, 0.0)
        sup_nodes.append(n+nodes_frame)
        Members_in_Set = []

        if kst_kol==0:
            EffLengthMembers[1].append(m+members_frame-kst_kol)
            DesignPropsViaParentSet = False
        else: DesignPropsViaParentSet = True

        if kst_kol >= 1:
            for k in range(kst_kol):
                Node(n+nodes_frame-k-1, i*dx, b, (k+1)*(h-h_dr)/(kst_kol+1))
                Member(m+members_frame-k,n+nodes_frame-k,n+nodes_frame-k-1, math.radians(90) ,1,1,params={'design_properties_via_member': False, 'design_properties_via_parent_member_set': True})
                Members_in_Set.append(m+members_frame-k)

                if i>0:
                    EffLengthMembers[2].append(i+nx*members_frame+(ny+kst_kol+1)*(nx-1)+k*(nx-1))
                    Member(i+nx*members_frame+(ny+kst_kol+1)*(nx-1)+k*(nx-1),n-k-1,n+nodes_frame-k-1,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

        Node(n+nodes_frame-kst_kol-1, i*dx, b, h-h_dr)
        Member(m+members_frame-kst_kol,n+nodes_frame-kst_kol,n+nodes_frame-kst_kol-1,math.radians(90),1,1,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})
        Members_in_Set.append(m+members_frame-kst_kol)

        #Randbalk maken
        if i>0:
            EffLengthMembers[2].append(i+nx*members_frame+(ny-1)*(nx-1))
            Member(i+nx*members_frame+(ny-1)*(nx-1),n-kst_kol-1,n+nodes_frame-kst_kol-1,math.radians(0),5,5,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

        if kst_kol >= 1:
            EffLengthSets[1].append(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET))
            MemberSet(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET), insertSpaces(Members_in_Set),SetType.SET_TYPE_CONTINUOUS,"Kolom",params={'design_properties_activated': True})

    #Hoofdliggers maken
        Members_in_Set = []

        if ny==2:
            EffLengthMembers[0].append(m+kst_kol+ny+1)
            DesignPropsViaParentSet = False
        else: DesignPropsViaParentSet = True

        if ny >= 3:
            Node(n+kst_kol+4, i*dx, dy, h-h_dr)
            Member(m+kst_kol+3,n+kst_kol+2,n+kst_kol+4, math.radians(0) ,3,3,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})
            Members_in_Set.append(m+kst_kol+3)

            #Kipsteun maken
            if i>0:
                EffLengthMembers[2].append(i+nx*members_frame+(0+1)*(nx-1))
                Member(i+nx*members_frame+(0+1)*(nx-1),n+kst_kol-nodes_frame+4,n+kst_kol+4,math.radians(0),6,6)

            for d in range(1,ny-2):
                Node(n+kst_kol+d+4, i*dx, (d+1)*dy, h-h_dr)
                EffLengthMembers[2].append(m+kst_kol+d+3)
                Member(m+kst_kol+d+3,n+kst_kol+d+3,n+kst_kol+d+4, math.radians(0) ,3,3)
                Members_in_Set.append(m+kst_kol+d+3)

                #Kipsteun maken
                if i>0:
                    EffLengthMembers[2].append(i+nx*members_frame+(d+1)*(nx-1))
                    Member(i+nx*members_frame+(d+1)*(nx-1),n+kst_kol-nodes_frame+d+4,n+kst_kol+d+4,math.radians(0),6,6)




        #Model.clientModel.service.finish_modification(); Model.clientModel.service.begin_modification()

        if ny==2:
            Member(m+kst_kol+ny+1,n+kst_kol+2,n+nodes_frame-kst_kol-1, math.radians(0) ,3,3,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})
        else:
            Member(m+kst_kol+ny+1,n+kst_kol+ny+1,n+nodes_frame-kst_kol-1, math.radians(0) ,3,3,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})

        #Model.clientModel.service.finish_modification(); Model.clientModel.service.begin_modification()

        Members_in_Set.append(m+kst_kol+ny+1)
        if ny >= 3:
            EffLengthSets[0].append(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET))
            MemberSet(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET), insertSpaces(Members_in_Set),SetType.SET_TYPE_CONTINUOUS,"Hoofdligger",params={'design_properties_activated': True})

    #Dakrand verticale en horizontale profielen maken
        Node(n+kst_kol+3, i*dx, 0, h)
        EffLengthMembers[3].append(m+kst_kol+2)
        Member(m+kst_kol+2,n+kst_kol+2,n+kst_kol+3, math.radians(90) ,9,9)
        if i>0:
            EffLengthMembers[2].append(i+nx*members_frame+(ny+kst_kol)*(nx-1))
            Member(i+nx*members_frame+(ny+kst_kol)*(nx-1),n+kst_kol+3-nodes_frame,n+kst_kol+3,math.radians(0),10,10)

        Node(n+nodes_frame-kst_kol-2, i*dx, b, h)
        EffLengthMembers[3].append(m+members_frame-kst_kol-1)
        Member(m+members_frame-kst_kol-1,n+nodes_frame-kst_kol-1,n+nodes_frame-kst_kol-2,math.radians(90),9,9)
        if i>0:
            EffLengthMembers[2].append(i+nx*members_frame+(ny+2*kst_kol+1)*(nx-1))
            Member(i+nx*members_frame+(ny+2*kst_kol+1)*(nx-1),n-kst_kol-2,n+nodes_frame-kst_kol-2,math.radians(0),10,10)

    #Kopse gevels
    #Op x=0 goldt eerder n = 0 en m = 0
    #Op x=L goldt eerder n = (nx-1)*nodes_frame en m = (nx-1)*members_frame

    n = nx*nodes_frame
    m = nx*members_frame+(ny+2*(kst_kol+1))*(nx-1)

    if ny >= 3:
        for d in range(ny-2):

            #Kolommen as x=0 (kopse gevel)
            Members_in_Set = []
            Node(n+d*(kst_kol+2)+1, 0.0, (d+1)*dy, 0.0)
            sup_nodes.append(n+d*(kst_kol+2)+1)

            if kst_kol==0:
                EffLengthMembers[1].append(m+d*(kst_kol+2)+kst_kol+1)
                DesignPropsViaParentSet = False
            else: DesignPropsViaParentSet = True

            if kst_kol >= 1:
                for k in range(kst_kol):
                    Node(n+d*(kst_kol+2)+k+2, 0.0, (d+1)*dy, (k+1)*(h-h_dr)/(kst_kol+1))
                    Member(m+d*(kst_kol+2)+k+1,n+d*(kst_kol+2)+k+1,n+d*(kst_kol+2)+k+2, math.radians(0) ,2,2,params={'design_properties_via_member': False, 'design_properties_via_parent_member_set': True})
                    Members_in_Set.append(m+d*(kst_kol+2)+k+1)

                    #Horizontale gevelliggers as x=0:
                    EffLengthMembers[2].append(m+d+1+2*(kst_kol+2)*(ny-2)+k*(ny-1))
                    if d==0:
                        Member(m+d+1+2*(kst_kol+2)*(ny-2)+k*(ny-1),0+1+k+1,n+d*(kst_kol+2)+k+2,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})
                    else:
                        Member(m+d+1+2*(kst_kol+2)*(ny-2)+k*(ny-1),n+(d-1)*(kst_kol+2)+k+2,n+d*(kst_kol+2)+k+2,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

            Member(m+d*(kst_kol+2)+kst_kol+1,n+d*(kst_kol+2)+kst_kol+1,0+kst_kol+d+4,math.radians(0),2,2,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})
            Members_in_Set.append(m+d*(kst_kol+2)+kst_kol+1)
            if kst_kol >= 1:
                EffLengthSets[1].append(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET))
                MemberSet(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET), insertSpaces(Members_in_Set),SetType.SET_TYPE_CONTINUOUS,"Kolom 2",params={'design_properties_activated': True})

            #Verticaal profiel dakrand x=0
            Node(n+d*(kst_kol+2)+kst_kol+2, 0.0, (d+1)*dy, h)
            EffLengthMembers[3].append(m+d*(kst_kol+2)+kst_kol+2)
            Member(m+d*(kst_kol+2)+kst_kol+2,0+kst_kol+d+4,n+d*(kst_kol+2)+kst_kol+2,math.radians(0),9,9,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

            #Horizontale profielen dakrand x=0
            EffLengthMembers[2].append(m+d+1+2*(kst_kol+2)*(ny-2)+kst_kol*(ny-1))
            if d==0:
                Member(m+d+1+2*(kst_kol+2)*(ny-2)+kst_kol*(ny-1),0+1+kst_kol+2,n+d*(kst_kol+2)+kst_kol+2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})
            else:
                Member(m+d+1+2*(kst_kol+2)*(ny-2)+kst_kol*(ny-1),n+d*(kst_kol+2),n+d*(kst_kol+2)+kst_kol+2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

            #Kolommen as x=L (kopse gevel)
            Members_in_Set = []
            Node(n+(ny-2+d)*(kst_kol+2)+1, (nx-1)*dx, (d+1)*dy, 0.0)
            sup_nodes.append(n+(ny-2+d)*(kst_kol+2)+1)

            if kst_kol==0:
                EffLengthMembers[1].append(m+(ny-2+d)*(kst_kol+2)+kst_kol+1)
                DesignPropsViaParentSet = False
            else: DesignPropsViaParentSet = True

            if kst_kol >= 1:
                for k in range(kst_kol):
                    Node(n+(ny-2+d)*(kst_kol+2)+k+2, (nx-1)*dx, (d+1)*dy, (k+1)*(h-h_dr)/(kst_kol+1))
                    Member(m+(ny-2+d)*(kst_kol+2)+k+1,n+(ny-2+d)*(kst_kol+2)+k+1,n+(ny-2+d)*(kst_kol+2)+k+2, math.radians(0) ,2,2,params={'design_properties_via_member': False, 'design_properties_via_parent_member_set': True})
                    Members_in_Set.append(m+(ny-2+d)*(kst_kol+2)+k+1)

                    #Horizontale gevelliggers as x=L:
                    EffLengthMembers[2].append(m+d+1+2*(kst_kol+2)*(ny-2)+(kst_kol+k+1)*(ny-1))
                    if d==0:
                        Member(m+d+1+2*(kst_kol+2)*(ny-2)+(kst_kol+k+1)*(ny-1),(nx-1)*nodes_frame+1+k+1,n+(ny-2+d)*(kst_kol+2)+k+2,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})
                    else:
                        Member(m+d+1+2*(kst_kol+2)*(ny-2)+(kst_kol+k+1)*(ny-1),n+(ny-2+d-1)*(kst_kol+2)+k+2,n+(ny-2+d)*(kst_kol+2)+k+2,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

            Member(m+(ny-2+d)*(kst_kol+2)+kst_kol+1,n+(ny-2+d)*(kst_kol+2)+kst_kol+1,(nx-1)*nodes_frame+kst_kol+d+4,math.radians(0),2,2,params={'design_properties_via_member': not DesignPropsViaParentSet, 'design_properties_via_parent_member_set': DesignPropsViaParentSet})
            Members_in_Set.append(m+(ny-2+d)*(kst_kol+2)+kst_kol+1)
            if kst_kol >= 1:
                EffLengthSets[1].append(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET))
                MemberSet(FirstFreeIdNumber(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET), insertSpaces(Members_in_Set),SetType.SET_TYPE_CONTINUOUS,"Kolom 2",params={'design_properties_activated': True})

            #Verticaal profiel dakrand x=L
            Node(n+(ny-2+d)*(kst_kol+2)+kst_kol+2, (nx-1)*dx, (d+1)*dy, h)
            EffLengthMembers[3].append(m+(ny-2+d)*(kst_kol+2)+kst_kol+2)
            Member(m+(ny-2+d)*(kst_kol+2)+kst_kol+2,(nx-1)*nodes_frame+kst_kol+d+4,n+(ny-2+d)*(kst_kol+2)+kst_kol+2,math.radians(0),9,9,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

            #Horizontale profielen dakrand x=L
            EffLengthMembers[2].append(m+d+1+2*(kst_kol+2)*(ny-2)+(2*kst_kol+1)*(ny-1))
            if d==0:
                Member(m+d+1+2*(kst_kol+2)*(ny-2)+(2*kst_kol+1)*(ny-1),(nx-1)*nodes_frame+1+kst_kol+2,n+(ny-2+d)*(kst_kol+2)+kst_kol+2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})
            else:
                Member(m+d+1+2*(kst_kol+2)*(ny-2)+(2*kst_kol+1)*(ny-1),n+(ny-2+d)*(kst_kol+2),n+(ny-2+d)*(kst_kol+2)+kst_kol+2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False})

        #Horizontale gevelliggers in de kopgevels die aansluiten bij y = b:
        for k in range(kst_kol):
            EffLengthMembers[2].append(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+k*(ny-1))
            Member(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+k*(ny-1),n+((ny-2)-1)*(kst_kol+2)+k+2,nodes_frame-k-1,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False}) #x=0
            EffLengthMembers[2].append(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+(kst_kol+k+1)*(ny-1))
            Member(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+(kst_kol+k+1)*(ny-1),n+(ny-2+(ny-2)-1)*(kst_kol+2)+k+2,(nx-1)*nodes_frame+nodes_frame-k-1,math.radians(0) ,8,8,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False}) #x=L

        #Horizontale profielen dakrand in de kopgevels die aansluiten bij y=b
        EffLengthMembers[2].append(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+kst_kol*(ny-1))
        Member(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+kst_kol*(ny-1),n+((ny-2)-1)*(kst_kol+2)+kst_kol+2,nodes_frame-kst_kol-2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False}) #x=0
        EffLengthMembers[2].append(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+(2*kst_kol+1)*(ny-1))
        Member(m+(ny-2)+1+2*(kst_kol+2)*(ny-2)+(2*kst_kol+1)*(ny-1),n+(ny-2+(ny-2))*(kst_kol+2),nx*nodes_frame-kst_kol-2,math.radians(0) ,10,10,params={'design_properties_via_member': True, 'design_properties_via_parent_member_set': False}) #x=L

    NodalSupport(1, insertSpaces(sup_nodes), [inf, inf, inf, 0.0, 0.0, inf])

    #----------------------------------------------------------------------------
    #-                      WINDVERBANDEN TOEVOEGEN                             -
    #----------------------------------------------------------------------------


    nodes = MFE_getNodes.getNodes()             # met deze lijst kan je knopen opzoeken op basis van hun coördinaten
    members = MFE_getMembers.getMembers()       # met deze lijst kan je staven opzoeken op basis van hun begin- en eindknoop

    Node1 = MFE_ZoekNode.ZoekNode(5,5,6,Model,nodes) #VOORBEELD van het zoeken van een knoop
    Node2 = MFE_ZoekNode.ZoekNode(5,10,6,Model,nodes) #VOORBEELD van het zoeken van een knoop

    print(Node1["no"])
    print(Node2["no"])


#TODO: elif toevoegen dat er nog wel horizontale gevelliggers en dakrandligger moeten worden tegevoegd als ny=2

    #Instellingen Steel Effective Lengths voor hoofdliggers maken:
    NodalSupportsList = []
    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])
    for i in range(5):
        NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, \
                                    SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, 1,4,2,3, \
                                    SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
                                    SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                    ""],)

    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])

    SteelEffectiveLengths(1, insertSpaces(EffLengthMembers[0]), insertSpaces(EffLengthSets[0]), False, False, False, True, True, False, 'SEL1', NodalSupportsList, intermediate_nodes=True,
                          different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE)

    #Instellingen Steel Effective Lengths voor kolommen maken:
    NodalSupportsList = []
    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])
    for i in range(5):
        NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, \
                                    SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                    SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
                                    SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                    ""],)

    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])

    SteelEffectiveLengths(2, insertSpaces(EffLengthMembers[1]), insertSpaces(EffLengthSets[1]), False, False, False, True, True, False, 'SEL2', NodalSupportsList, intermediate_nodes=True,
                          different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE)

    #Instellingen Steel Effective Lengths voor andere liggers maken:
    NodalSupportsList = []
    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])

    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])

    SteelEffectiveLengths(3, insertSpaces(EffLengthMembers[2]), insertSpaces(EffLengthSets[2]), False, False, False, True, True, False, 'SEL3', NodalSupportsList, intermediate_nodes=False,
                          different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE)

    #Instellingen Steel Effective Lengths voor verticale dakrandprofielen maken:
    NodalSupportsList = []
    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_YES, \
                                ""])

    NodalSupportsList.append([SteelEffectiveLengthsSupportType.SUPPORT_TYPE_NONE, True, 0.0, \
                                SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, 0,0,0,0, \
                                SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
                                SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, \
                                ""])

    SteelEffectiveLengths(4, insertSpaces(EffLengthMembers[3]), insertSpaces(EffLengthSets[3]), False, False, False, True, True, False, 'SEL4', NodalSupportsList, intermediate_nodes=False,
                          different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE)

    SteelDesignUltimateConfigurations(1, name="EC3 checks UGT")
    SteelDesignServiceabilityConfigurations(1,"EC3 checks BGT")
    #BeamLimitCharacteristic(134,1)

    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")

#BELASTINGEN

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

    Model.clientModel.service.finish_modification()

    LoadCase.StaticAnalysis(10, 'PB: Eigen Gewicht',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[True, 0.0, 0.0, -1.0])

    LoadCase.StaticAnalysis(20, 'PB: Vloerafwerking en dakbedekking',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(30, 'PB: Gevelbekleding',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(40, 'PB: Trappen, leuningen en bordessen',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(50, 'PB: Klein installatie werk (gelijkmatig verdeeld)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    LoadCase.StaticAnalysis(60, 'PB: Grote leidingen en leidingsupports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    LoadCase.StaticAnalysis(70, 'PB: Overige supports',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, self_weight=[False])
    LoadCase.StaticAnalysis(80, 'PB: Gronddrukken',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(90, 'PB: Reserve',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, self_weight=[False])
    LoadCase.StaticAnalysis(100, 'VB: Opgelegde belasting op vloeren (momentaan)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_E_STORAGE_AREAS_QI_E, self_weight=[False])
    LoadCase.StaticAnalysis(300, 'VB: Sneeuw en/of aanvriezing',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_SNOW_ICE_LOADS_H_LESS_OR_EQUAL_TO_1000_M_QS, self_weight=[False])
    LoadCase.StaticAnalysis(401, 'VB: Wind (+X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(402, 'VB: Wind (-X richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(403, 'VB: Wind (+Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
    LoadCase.StaticAnalysis(404, 'VB: Wind (-Y richting)',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_WIND_QW, self_weight=[False])
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

    SnowWizardMonopitch([4,9,57,52])