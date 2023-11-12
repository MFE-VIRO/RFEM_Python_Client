from RFEM.enums import CaseObjectType
from RFEM.initModel import Model
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue

Naam_Model = "MFE_HAL.rf6"
StaafNummer = 17
parameter = 'internal_force_vz'

Model(False,Naam_Model)

MIF = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,1,StaafNummer)
MIFSet = ResultTables.MembersInternalForcesByMemberSet(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,1,5)
MIFS = ResultTables.MembersInternalForcesBySection(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION,2,4,True)

MinV = f'{GetMinValue(MIF,parameter):.2f}' # f string formatting voor 2 decimale getallen
MaxV = f'{GetMaxValue(MIF,parameter):.2f}' # f string formatting voor 2 decimale getallen
MinVs = f'{GetMinValue(MIFSet,parameter):.2f}' # f string formatting voor 2 decimale getallen
MaxVs = f'{GetMaxValue(MIFSet,parameter):.2f}' # f string formatting voor 2 decimale getallen
print("MIF staaf " + str(StaafNummer) + ":")
print("Min. waarde " + parameter + ":" + MinV)
print("Max. waarde " + parameter + ":" + MaxV)
print("Min. waarde " + parameter + "Set 5:" + MinVs)
print("Max. waarde " + parameter + "Set 5:" + MaxVs)
# print(f'{GetMaxValue(MIF,"internal_force_n"):.2f}') # f string formatting voor 2 decimale getallen
print(GetMinValue(MIFS,parameter))
print(GetMaxValue(MIFS,parameter))

print("einde")