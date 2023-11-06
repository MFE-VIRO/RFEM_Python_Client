from suds.client import Client
from suds impo
import sys

client = Client('http://localhost:8081/wsdl')
# printout all application functions and types
print(client)
modelLst = client.service.get_model_list()
new = client.service.get_active_model()+'wsdl'
model = Client(new)
# printout all model functions and types
print(client.get_combination_wizard)