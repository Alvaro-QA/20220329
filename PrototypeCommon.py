import os.path
import re
import time
import unittest

from selenium import webdriver
import json
from os import walk

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Logger import Logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PrototypeCommon(unittest.TestCase):
    pathApp = "C:\\Users\\hgarau\\Documents\\Visual Studio 2015\\Projects\\puntacaja_net-release-2.15.0\\puntacaja_net-release-2.15.0\\SirisMVC\\UseMVCApplication\\bin\\Debug\\SirisNet.exe"
    ignore_errors = False
    oLogger = {}
    ERROR_NAME_CORTE_CAJA = "SE HA SUPERADO EL LIMITE DE EFECTIVO EN SU TERMINAL. REALICE UN CORTE DE CAJA PARA PODER SEGUIR OPERANDO.\n"

    def setUp(self):
        desired_caps = {}
        desired_caps[ "app"] = self.pathApp
        desired_caps["ms:waitForAppLaunch"] = "5"
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
        self.oLogger = Logger('','logs\\' + time.strftime("%y%m%d_%H%M%S") + '\\')
        os.mkdir(self.oLogger.pathName + '\\img')


    def login(self,data):
        if isinstance(data,str):
            os.path.isfile(data)
            data = self.loadFromJSon(data)

        self.logger("LOGIN")

        self.driver.find_element_by_name("Usuario:").send_keys(data["usuario"] + Keys.TAB + data["clave"])

        try:
            self.driver.find_element_by_name("Confirmar <F2>").click()
        except:
            self.logger('Fallo login','fallo_login.jpg')
            self.driver.find_elements_by_name("OK").click()
            return -1

    def loadFromJSon(self,fileName):
        fd = open(fileName)
        data = json.load(fd)
        fd.close()
        return data

    def terminar(self):
        self.driver.quit()

    def buildJSON(self, params):
        data = {}
        for param in params:
            if param['value'][1] == '[' and param['value'][-1] == ']':
                data[param['reference']] = param['value'][1:-1].partition(',')
            else:
                data[param['reference']] = param['value']
        return data
    def Myfail(self,msg):
        if not self.ignore_errors:
            self.driver.close()
            self.driver.quit()
            self.fail(msg)
    def screenShot(self,name):
        time.sleep(2)
        self.driver.save_screenshot(name)

    def logger(self,msg,fileName = ''):
        self.oLogger.logger(msg)
        if(fileName != ''):
            self.screenShot(self.oLogger.pathName + 'img\\' + time.strftime("%y%m%d_%H%M%S") + '_' + fileName)