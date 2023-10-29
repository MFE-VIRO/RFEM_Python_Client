from suds.client import Client

client = Client('http://localhost:8081/wsdl')
new = client.service.get_active_model()+'wsdl'
model = Client(new)

print(model.service.get_surface(1))