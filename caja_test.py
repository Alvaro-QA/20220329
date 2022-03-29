import requests

import PrototypeCaja

class CajaTests(PrototypeCaja.PrototypeCaja):
	pathCarritos = 'carritos_7105'
	pathApp = "C:\\Users\\hgarau\\Desktop\\caja\\SirisNet.exe"
	fileAbrirJSON = 'data\\caja_test\\abrir_caja.json'
	fileCerrarJSON = 'data\\caja_test\\cerrar_caja.json'
	fileCorteJSON = 'data\\caja_test\\corte_caja.json'
	fileErrorLimiteCorteJSON = 'data\\caja_test\\errors\\limite_corte_caja.json'
	fileLoginJSON = 'data\\login.json'
	fileLoginTesoreriaJSON = 'data\\loginTesoreria.json'
	ignore_errors = False
	def test_abrir_recaudar_cerrar(self):
		self.login(self.fileLoginJSON)
		self.abrirCaja(self.fileAbrirJSON, self.fileLoginTesoreriaJSON)
		self.recaudar(self.pathCarritos)
		self.cerrarCaja(self.fileCerrarJSON, self.fileLoginTesoreriaJSON)
		self.terminar()

	def test_corte(self):
		self.login(self.fileLoginJSON)
		self.corteCaja(self.fileCorteJSON, self.fileLoginTesoreriaJSON)
		self.terminar()
	#
	# def test_custom(self):
	# 	url = 'http://localhost:8000/'
	# 	response = requests.get(url + 'test/2')
	# 	testJSON = response.json()['data']
	#
	# 	for step in testJSON['steps']['data']:
	# 		method_to_call = getattr(self, step['step']['method'])
	# 		params = self.buildJSON(step['params'])
	# 		if step['step']['method'] != 'abrirCaja':
	# 			method_to_call(params)
	# 		else:
	# 			method_to_call()
