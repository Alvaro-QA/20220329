import time
import unittest

from selenium import webdriver
import json
from os import walk

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import PrototypeCommon

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PrototypeCaja(PrototypeCommon.PrototypeCommon):
    pathApp = "C:\\Users\\hgarau\\Documents\\Visual Studio 2015\\Projects\\puntacaja_net-release-2.15.0\\puntacaja_net-release-2.15.0\\SirisMVC\\UseMVCApplication\\bin\\Debug\\SirisNet.exe"

    def recaudar(self, JSON):
        self.inicioRecaudacion()
        self.readFromPathJSON(JSON)

    def inicioRecaudacion(self):
        self.driver.find_element_by_name("Operaciones").click()
        self.driver.find_element_by_name("Recaudaciones").click()

    def inicioAbrir(self):
        self.driver.find_element_by_name("Herramientas").click()
        self.driver.find_element_by_name("Abrir Caja").click()

    def inicioCerrar(self):
        menu = self.driver.find_element_by_name("Operaciones")
        menu.click()
        menu.send_keys(Keys.CONTROL, Keys.F3)

    def inicioCorte(self):
        menu = self.driver.find_element_by_name("Operaciones")
        menu.click()
        action = ActionChains(self.driver)
        action.move_to_element(menu)
        action.click(self.driver.find_element_by_name("Corte de Caja"))
        action.perform()


    def abrirCaja(self, fileJSON, fileJSONLoginTesoreria):
        self.inicioAbrir()
        data = self.loadFromJSon(fileJSON)
        try:
            self.driver.find_elements_by_name("USD $ 0")[0].send_keys(Keys.CONTROL, "a")
            self.driver.find_elements_by_name("USD $ 0")[0].send_keys(data["Importe"])
            self.logger("Abrir caja","abrir_caja.jpg")
            self.driver.find_element_by_name("Confirmar <F2>").click()
        except:
            self.logger("Fallo Abrir caja","fallo_abrir_caja.jpg")
            self.driver.find_element_by_name("OK").click()
            self.Myfail('Fallo en abrir caja')
            return -1
        if self.driver.find_elements_by_name("Yes"):
            self.driver.find_element_by_name("Yes").click()
            self.login(fileJSONLoginTesoreria)
        self.driver.find_element_by_name("OK").click()

    def corteCaja(self, fileJSON,fileLoginTesoreriaJSON ):
        self.inicioCorte()
        data = self.loadFromJSon(fileJSON)
        firstElement = self.driver.find_elements_by_name("Efectivo")[1]
        if data['tipo'] == 'C': #destildo y pasa a cheque
            firstElement.click()
        # asumo que todas las variables existen
        acciones = Keys.TAB + Keys.TAB + data["cantidad"]
        acciones += Keys.TAB + data["efectivo"]
        #acciones += Keys.TAB + data["destino"]
        firstElement.send_keys(acciones)

        self.logger("Corte caja", "corte_caja.jpg")
        self.driver.find_element_by_name("Confirmar <F2>").click()
        self.driver.find_element_by_name("OK").click()
        self.login(fileLoginTesoreriaJSON)
        self.driver.find_element_by_name("OK").click()


    def cerrarCaja(self, fileJSON, fileJSONLoginTesoreria):
        self.inicioCerrar()
        data = self.loadFromJSon(fileJSON)
        time.sleep(2)
        self.driver.find_element_by_name("Ingrese monto efectivo en caja:").send_keys(Keys.CONTROL, "a")
        self.driver.find_element_by_name("Ingrese monto efectivo en caja:").send_keys(data["Importe"] + Keys.F2)
        self.logger("Cerrar caja", "cerrar_caja.jpg")
        self.driver.find_element_by_name("Confirmar <F2>").click()
        if self.driver.find_elements_by_name("Usuario:"):
            self.login(fileJSONLoginTesoreria)
        else:
            self.driver.find_element_by_name("Yes").click()
        time.sleep(2)
        self.driver.find_element_by_name("OK").click()

    def readFromJSON(self, fileJSON):
        self.logger('Leyendo ' + fileJSON)
        fd = open(fileJSON)
        data = json.load(fd)
        fd.close()
        for operacion in data:
            if "inactivo" in operacion and operacion["inactivo"]:
                self.logger('No procesado por inactivo')
                return 0
            for dato in operacion["datos"]:
                waitFor = []
                for k in dato:
                    self.logger(k + ': ' + dato[k])
                    if len(waitFor) > 0 and k not in waitFor.index(k):
                        continue
                    waitFor = []
                    try:
                        if len(self.driver.find_elements_by_name(self.ERROR_NAME_CORTE_CAJA)) > 0:
                            self.logger('Se requiere corte')
                            self.corteCaja(self.fileErrorLimiteCorteJSON, self.fileLoginTesoreriaJSON)
                            return -1
                        self.interpretarOperacionJSON(k, dato[k])
                    except:
                        try:
                            self.driver.find_element_by_name("Confirmar").click()
                            try:
                                self.interpretarOperacionJSON(k, dato[k])
                            except:
                                self.logger('Excepcion inesperada 2', 'error_readFromJSON_2.jpg')
                                waitFor = ['*','Ingrese código de barras']
                                continue
                        except:
                            self.logger('Excepcion inesperada', 'error_readFromJSON_1.jpg')
                            self.Myfail('error en la recaudacion 1')
                    if k != '*':
                        self.driver.find_element_by_name("Confirmar").click()
        try:
            self.logger('Empieza pago')
            self.driver.find_element_by_name("Confirmar <F2>").click()
            self.driver.find_elements_by_name("Efectivo")[1].click()
            self.logger('Pagar carrito', 'pagar_carrito' + fileJSON[fileJSON.find('\\') + 1:] + '.jpg')
            self.driver.find_element_by_name("Confirmar <F2>").click()
        except:
            self.logger('Excepcion inesperada', 'error_pagar.jpg')
            return 0
            #self.Myfail('Error en fin recaudacion')
        return 1

    def interpretarOperacionJSON(self, campo, valor):

        if campo == '*':  # boton
            self.driver.find_element_by_name(valor).click()
        else:  # busca btn confimar despues de la accion
            if campo != '_':  # texto
                if campo[0] == '#':
                    self.driver.find_element_by_id(campo[1:]).send_keys(valor)
                else:
                    self.driver.find_element_by_name(campo).send_keys(valor)


    def readFromPathJSON(self,pathJSON,fileInicioJSON = ''):
        f = []
        for (dirpath, dirnames, filenames) in walk(pathJSON ):
            f.extend(filenames)
            break
        for fileJSON in f:
            if fileInicioJSON != '' and fileInicioJSON != fileJSON:
                continue
            fileInicioJSON = ''
            if fileJSON[0] != '_':
                if self.readFromJSON(pathJSON + "\\" + fileJSON) == -1:
                    self.inicioRecaudacion()
                    self.readFromPathJSON(pathJSON, fileJSON)
                    return -1
            else:
                self.logger(fileJSON + ': No procesado _')