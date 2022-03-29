import logging
import os.path
import unittest

from selenium import webdriver
import json
from os import walk

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import PrototypeCommon

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PrototypeTeso(PrototypeCommon.PrototypeCommon):
    pathApp = "C:\\Users\\hgarau\\Documents\\Visual Studio 2015\\Projects\\puntacaja_net-release-2.15.0\\puntacaja_net-release-2.15.0\\SirisMVC\\UseMVCApplication\\bin\\Debug\\SirisNet.exe"

    fileGestionJSON = "data\\teso_test\\gestion_cajas.json"

    def inicioAbrir(self):
        self.driver.find_element_by_name("Herramientas").click()
        self.driver.find_element_by_name("Abrir agencia").click()

    def abrirCaja(self):
        self.inicioAbrir()
        self.logger("ABRIR AGENCIA",'abrir_agencia.jpg')
        self.driver.find_element_by_name("Confirmar <F2>").click()
        if self.driver.find_elements_by_name("Yes"):
            self.driver.find_element_by_name("Yes").click()
            self.login()
        self.driver.find_element_by_name("OK").click()

    def gestionCajas(self, data):
        self.inicioGestionCajas()

        if isinstance(data,str):
            os.path.isfile(data)
            data = self.loadFromJSon(data)

        for i in range(0, 10): #asumo que no hay as de 50 terminales
            logging.info(str(i))
            try:
                rowTerminal = self.driver.find_element_by_name("Nro terminal Row " + str(i))
            except NoSuchElementException:
                break
            if rowTerminal.text in data["Habilitadas"]:
                try:
                    if self.driver.find_element_by_name("Habilitada Row " + str(i)).text == 'False':
                        self.switchTerminal(rowTerminal)
                except NoSuchElementException:
                    self.switchTerminal(rowTerminal)
            else:
                if rowTerminal.text in data["Deshabilitadas"]:
                    try:
                        if self.driver.find_element_by_name("Habilitada Row " + str(i)).text == 'True':
                            self.switchTerminal(rowTerminal)
                    except NoSuchElementException:
                        pass
        self.logger('Gestion de agencias','gestion_agencia.jpg')
        self.driver.find_element_by_name("Guardar <F2>").click()
        self.driver.find_element_by_name("Yes").click()
        self.driver.find_element_by_name("OK").click()

    def switchTerminal(self, rowTerminal):
        ac = ActionChains(self.driver)
        rowTerminal.click()
        ac.move_to_element(rowTerminal) \
            .key_down(Keys.SHIFT) \
            .send_keys(Keys.TAB + Keys.TAB + Keys.TAB ) \
            .key_up(Keys.SHIFT) \
            .send_keys(Keys.SPACE) \
            .perform()

    def inicioGestionCajas(self):
        menu = self.driver.find_element_by_name("Herramientas")
        menu.click()
        menu.send_keys(Keys.ARROW_DOWN + Keys.ARROW_DOWN + Keys.ENTER)

    def inicioCerrar(self):
        menu = self.driver.find_element_by_name("Operaciones")
        menu.click()
        menu.send_keys(Keys.CONTROL, Keys.F3)


