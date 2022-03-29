
import PrototypeCaja

class RecaudacionTests(PrototypeCaja.PrototypeCaja):
	pathCarritos = 'carritos'
	fileLoginJSON = 'data\\login.json'
	fileLoginTesoreriaJSON = 'data\\loginTesoreria.json'
    
	def test_simple(self):
		self.login(self.fileLoginJSON)
		self.inicioRecaudacion()
		self.readFromPathJSON(self.pathCarritos)
		self.terminar()


