from RFEM.enums import CaseObjectType
from RFEM.initModel import Model
from RFEM.Results.resultTables import ResultTables, GetMaxValue, GetMinValue

Naam_Model = "MFE_HAL.rf6"
StaafNummer = 17
parameter = 'internal_force_vz'

Model(False,Naam_Model)

MIF = ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,1,StaafNummer)
MIFS = ResultTables.MembersInternalForcesBySection(CaseObjectType.E_OBJECT_TYPE_DESIGN_SITUATION,1,3,True)
MinV = f'{GetMinValue(MIF,parameter):.2f}' # f string formatting voor 2 decimale getallen
MaxV = f'{GetMaxValue(MIF,parameter):.2f}' # f string formatting voor 2 decimale getallen
print("MIF staaf " + str(StaafNummer) + ":")
print("Min. waarde " + parameter + ":" + MinV)
print("Max. waarde " + parameter + ":" + MaxV)
# print(f'{GetMaxValue(MIF,"internal_force_n"):.2f}') # f string formatting voor 2 decimale getallen
print(GetMinValue(MIFS,parameter))
print(GetMaxValue(MIFS,parameter))

print("einde")