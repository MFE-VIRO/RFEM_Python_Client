import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RFEM.BasicObjects.node import Node
from RFEM.formula import Formula
from RFEM.globalParameter import GlobalParameter
from RFEM.initModel import Model, getPathToRunningRFEM
from RFEM.enums import FormulaParameter, GlobalParameterUnitGroup, GlobalParameterDefinitionType, ObjectTypes

Model(False,"NewTemplate_IMP")

Model.clientModel.service.begin_modification()
GlobalParameter.AddParameter(
                                 no= 5,
                                 name= 'Test_2',
                                 symbol= 'Test_1',
                                 unit_group= GlobalParameterUnitGroup.LENGTH,
                                 definition_type= GlobalParameterDefinitionType.DEFINITION_TYPE_FORMULA,
                                 definition_parameter= ['1+1'],
                                 comment= 'Comment_1')

Model.clientModel.service.finish_modification()

gp_1 = Model.clientModel.service.get_global_parameter(1)
gp_1.no = 3

Model.clientModel.service.begin_modification()
GlobalParameter.AddParameter(
                                 no= gp_1.no,
                                 name= gp_1.name,
                                 symbol= gp_1.symbol,
                                 unit_group= gp_1.unit_group,
                                 definition_type= gp_1.definition_type,
                                #  definition_parameter= gp_1.definition_parameter,
                                 comment= gp_1.comment)

Model.clientModel.service.finish_modification()