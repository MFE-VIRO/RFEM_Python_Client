from RFEM.initModel import *
from RFEM.enums import *

class SolidLoad():

    def __init__(self,
                 no: int =1,
                 load_case_no: int = 1,
                 solids_no: str= '1',
                 load_type = SolidLoadType.LOAD_TYPE_FORCE,
                 load_distribution = SolidLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                 load_direction = SolidLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE,
                 magnitude: float = 0,
                 comment: str = '',
                 params: dict = {}):
        
        # Client model | Solid Load
        clientObject = clientModel.factory.create('ns0:solid_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Solid No.
        clientObject.solids = ConvertToDlString(solids_no)
        
        # Load Type
        clientObject.load_type = load_type.name

        # Load Distribution
        clientObject.load_distribution = load_distribution.name

        # Load Direction
        clientObject.load_direction = load_direction.name

        # Load Magnitude
        clientObject.uniform_magnitude = magnitude
        
        # Comment
        clientObject.comment = comment
        
        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Solid Load to client model
        clientModel.service.set_solid_load(load_case_no, clientObject)
        

    def Force():
        # Siehe lineLoad.Force()
        pass

    def Temperature():
        # Siehe memberLoad.Temperature()
        pass

    def Strain():
        pass

    def Motion():
        pass

    def Buoyancy():
        pass

    def Gass():
        pass