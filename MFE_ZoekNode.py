import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/../..')

from suds.client import Client
import sys
from RFEM.enums import CaseObjectType
from RFEM.enums import *
from RFEM.initModel import Model, ConvertStrToListOfInt, ConvertToDlString, GetModelMainParameters, GetName,getPathToRunningRFEM, GetModelId, GetModelParameters
from RFEM.BasicObjects.node import Node
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType, GetAllObjects

from RFEM.Tools.GetObjectNumbersByType import GetAllObjects

import time

#------------------------------------------------------------------------
#-  UITPROBEERSEL: AANROEPEN CURRENT MODEL ALS JE DE NAAM NIET WEET     -
#------------------------------------------------------------------------

# client = Client('http://localhost:8081/wsdl')
# print(client.service.get_model_list)
# new = client.service.get_active_model()+'wsdl'
# model = Client(new)
# sup = model.service.get_nodal_support(1)

#------------------------------------------------------------------------

def ZoekNode(
        x : float = 0.0,
        y : float = 0.0,
        z : float = 0.0,
        model = Model):

    NodeNumbers = GetObjectNumbersByType(ObjectType=ObjectTypes.E_OBJECT_TYPE_NODE)
    xd = x
    yd = y
    zd = z

    afw = 6   #=toelaatbare afwijking van coordinaat in meters

    fNodes = [] #=lijst voor gevonden knopen waarvan de coordinaten overeenkomen

    time1 = time.time() #Begintijd onthouden om inzicht te krijgen in de benodigde tijd voor een bepaald gedeelte van de code

    while True:
        fNodes.clear()
        min_afwi = 100
        for i in NodeNumbers:
            node = Node.GetNode(i)
            noi = node.no
            xi = node.coordinate_1
            yi = node.coordinate_2
            zi = node.coordinate_3
            if xi >= xd-afw and xi <= xd+afw:
                if yi >= yd-afw and yi <= yd+afw:
                    if zi >= zd-afw and zi <= zd+afw:
                        afwi = ((xi-xd)**2+(yi-yd)**2+(zi-zd)**2)**(1/2)
                        if (afwi <= afw):
                            fNodes.append(node)
                        min_afwi = min(min_afwi,afwi)
        if len(fNodes)==1: break
        afw = min_afwi


    # time2 = time.time() #Eindtijd van het gedeelte van de code waarvan ik wil weten hoe lang het duurt
    # dtime = time2 - time1 #Tijd die het gedeelte van de code heeft geduurd in seconde
    # print(str(dtime) + " s") #Afdrukken benodigde tijd

    # print(fNodes[0].no)
    # print("afw" + str(afw))
    return fNodes[0]

def ZoekNode2(
        x : float = 0.0,
        y : float = 0.0,
        z : float = 0.0,
        model = Model,
        nodes = []):

    xd = x
    yd = y
    zd = z

    afw = 6   #=toelaatbare afwijking van coordinaat in meters

    fNodes = [] #=lijst voor gevonden knopen waarvan de coordinaten overeenkomen

    time1 = time.time() #Begintijd onthouden om inzicht te krijgen in de benodigde tijd voor een bepaald gedeelte van de code

    while True:
        fNodes.clear()
        min_afwi = 100
        for node in nodes:
            noi = node["no"]
            xi = node["x"]
            yi = node["y"]
            zi = node["z"]
            if xi >= xd-afw and xi <= xd+afw:
                if yi >= yd-afw and yi <= yd+afw:
                    if zi >= zd-afw and zi <= zd+afw:
                        afwi = ((xi-xd)**2+(yi-yd)**2+(zi-zd)**2)**(1/2)
                        if (afwi <= afw):
                            fNodes.append(node)
                        min_afwi = min(min_afwi,afwi)
        if len(fNodes)==1: break
        afw = min_afwi


    # time2 = time.time() #Eindtijd van het gedeelte van de code waarvan ik wil weten hoe lang het duurt
    # dtime = time2 - time1 #Tijd die het gedeelte van de code heeft geduurd in seconde
    # print(str(dtime) + " s") #Afdrukken benodigde tijd

    # print(fNodes[0].no)
    # print("afw" + str(afw))
    return fNodes[0]
