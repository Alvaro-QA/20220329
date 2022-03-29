import PrototypeCaja

class IniciarCajaTests(PrototypeCaja.PrototypeCaja):
	def test_abriCaja(self):
		self.login()
		self.driver.find_element_by_name("Herramientas").click()
		self.driver.find_element_by_name("Abrir Caja").click()
		try:
			self.driver.find_element_by_name("Confirmar <F2>").click()
		except:
			pass

		self.driver.switch_to.alert().accept()
