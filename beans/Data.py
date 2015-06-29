# -*- coding: utf-8 -*-
__author__ = 'fgh'


# dada de una estrella en una imatge
class Data:
    def __init__(self, x, y, sky, skyError, date):
        self.x = x                  # x pixel position of the star in the image
        self.y = y                  # y pixel position of the star in the image

        self.sky = sky
        self.skyError = skyError

        self.date = date

        self.apCounts = {}
        self.apErrors = {}


    def addCount(self, count, error, aper):
        self.apCounts[aper] = count
        self.apErrors[aper] = error



# FWHM    =                   2. / [pix] standard FWHM of objects
# NAPER   =                   12 / Count of apertures
# SAPER   =                    1 / Selected aperture (for processing)
# APER    =                   2. / [pix] radius of selected aperture
# APER1   =                   2. / [pix] aperture radius
# APER2   =               2.5583 / [pix] aperture radius
# APER3   =               3.2724 / [pix] aperture radius
# APER4   =               4.1858 / [pix] aperture radius
# APER5   =               5.3543 / [pix] aperture radius
# APER6   =               6.8488 / [pix] aperture radius
# APER7   =               8.7606 / [pix] aperture radius
# APER8   =               11.206 / [pix] aperture radius
# APER9   =               14.334 / [pix] aperture radius
# APER10  =               18.335 / [pix] aperture radius
# APER11  =               23.453 / [pix] aperture radius
# APER12  =                  30. / [pix] aperture radius
# ANNULUS1=                  14. / [pix] inner sky annulus radius
# ANNULUS2=                  35. / [pix] outer sky annulus radius
