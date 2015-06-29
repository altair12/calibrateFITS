# -*- coding: utf-8 -*-
__author__ = 'fgh'


# a part de posició ha de incloure caracteristiques del pic etc...
# radi estrella
# contes amb diferents radis

class Star:
    def __init__(self):
        self.datas = list()

    def addData(self, data):
        self.datas.append(data)

    def getLastData(self):
        return self.datas[-1]


#TODO: order data list by julian geocentric day