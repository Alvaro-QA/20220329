import logging
import os
import unittest
from distutils import command

import requests

import teso_test

class CustomTest(unittest.TestCase):
    def test_from_config(self):
        #os.system("pytest test_teso.TesoTests.test_abrir")
        url = 'http://localhost:8000/'
        response = requests.get(url + 'test/1')
        testJSON = response.json()['data']
        os.system('echo "Test: ' + testJSON['name'] + '"')

        stepsJSON = testJSON['steps']['data']
        for test_step in testJSON['steps']['data']:
            os.system('echo "metodo: ' + test_step['step']['method'] + '"')

        suite = unittest.TestSuite()
        suite.addTest(teso_test.TesoTests(stepsJSON))

#        suite = unittest.TestLoader().loadTestsFromTestCase(teso_test.TesoTests)
        unittest.TextTestRunner(verbosity=2).run(suite)

        assert 1 == response.json()['id']
