# -*- coding: utf-8 -*-
__author__ = 'fgh'

#Image que contè n estrelles
class Image:
    def __init__(self, name, date):
        self.name = name
        self.date = date

        self.dates = {}

    def addData(self, x, y, data):
        self.dates[(x,y)] = data

