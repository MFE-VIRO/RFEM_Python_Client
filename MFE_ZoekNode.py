from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.BasicObjects.node import Node

def ZoekNode(
        X : float = 0.0,
        Y : float = 0.0,
        Z : float = 0.0,
        model = Model,
        nodes = []):

    Xd = X
    Yd = Y
    Zd = Z

    afw = 6   #=toelaatbare afwijking van coordinaat in meters

    fNodes = [] #=lijst voor gevonden knopen waarvan de coordinaten overeenkomen

    while True:
        fNodes.clear()
        min_afwi = 100
        for node in nodes:
            noi = node["no"]
            Xi = node["X"]
            Yi = node["Y"]
            Zi = node["Z"]
            if Xi >= Xd-afw and Xi <= Xd+afw:
                if Yi >= Yd-afw and Yi <= Yd+afw:
                    if Zi >= Zd-afw and Zi <= Zd+afw:
                        afwi = ((Xi-Xd)**2+(Yi-Yd)**2+(Zi-Zd)**2)**(1/2)
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
