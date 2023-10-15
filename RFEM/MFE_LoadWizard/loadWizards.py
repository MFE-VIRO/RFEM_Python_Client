from RFEM.initModel import Model, clearAttributes, deleteEmptyAttributes

class SnowLoadWizard():

    def __init__(self,
                 no: int = 1,
                 comment: str = 'Comment',
                 params: dict = {
                    "standard_for_load_wizard": 6500
                 },
                 model= Model):

      clientObject = model.clientModel.factory.create('ns0:SnowLoadWizard')
      clearAttributes(clientObject)
      clientObject.no = no
      clientObject.comment = comment
      if params:
            for key in params:
                clientObject[key] = params[key]

      deleteEmptyAttributes(clientObject)
      model.clientModel.service.set_snow_load_wizard(clientObject)
      # standardCode = model.clientModel.service.get_load_cases_and_combinations().current_standard_for_combination_wizard

      # return actionCategoryDictionary[str(standardCode)]