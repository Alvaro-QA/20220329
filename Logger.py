import os
import time


class Logger:
    pathName = ""
    fileName = ""
    ds = {}
    def __init__(self, fileName = "" , pathName = "logs\\" ):
        if fileName == "":
            fileName = 'log_' + time.strftime("%y%m%d_%H%M%S") + '.txt'
        self.fileName = fileName
        self.pathName = pathName
        if not os.path.isdir(self.pathName):
            os.mkdir(self.pathName)
        self.ds = open(self.pathName + self.fileName, "a")

    def logger(self, msg):
        self.ds.write(msg + '\n')
