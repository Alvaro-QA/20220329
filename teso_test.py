
import requests
import PrototypeTeso

class TesoTests(PrototypeTeso.PrototypeTeso):
	pathCarritos = 'carritos_test_ticket_cierre'
	pathApp = "C:\\Users\\hgarau\\Desktop\\teso\\SirisNet.exe"
	fileCerrarJSON = 'data\\teso_test\\cerrar_caja.json'
	fileGestionCajasJSON = 'data\\teso_test\\gestion_cajas.json'
	fileLoginJSON = 'data\\loginTesoreria.json'
	stepJSON = []


##POR ARCHIVOS JSON
	def test_abrir(self):
		self.login(self.fileLoginJSON)
		self.abrirCaja()
		self.gestionCajas(self.fileGestionCajasJSON)
		self.terminar()

	## POR SERVICIO

	def test_custom(self):
		url = 'http://localhost:8000/'
		response = requests.get(url + 'test/1')
		testJSON = response.json()['data']

		for step in testJSON['steps']['data']:
			method_to_call = getattr(self, step['step']['method'])
			params = self.buildJSON(step['params'])
			if step['step']['method'] != 'abrirCaja':
				method_to_call(params)
			else:
				method_to_call()
