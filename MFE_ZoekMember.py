from RFEM.enums import *
from RFEM.initModel import Model
from RFEM.BasicObjects.member import Member

def ZoekNode(
        node_start : int = 1,
        node_end : int = 1,
        model = Model,
        members = []):

#LET OP: TODO: Als je laat zoeken op knopen, weet je niet wat de begin en wat de eindknoop is. Dit moet verwerkt worden in de routine!!!!

    fMembers = [] #=lijst voor gevonden staven met het genoemde begin en eindpunt

    for member in members:
        noi = member["no"]
        node_start_i = member["node_start"]
        node_end_i = member["node_end"]
        if node_start == node_start_i:
            if node_end == node_end_i:
                fMembers.append(member)

    if len(fMembers)==1: return fMembers[0]
    elif len(fMembers)==0: print("Er zijn geen staven met de gegeven begin- en/of eindknoop.")
    else: print("Er zijn meerdere staven met deze begin en eindknoop.")
