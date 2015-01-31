# -*- coding: utf-8 -*-
__author__ = 'fgh'

from astropy.io import fits

def getHeader(fname):
    hdus = fits.open(fname)
    header = hdus[0].header
    hdus.close()
    return header

def getHeaderValue(fname, param):
    header = getHeader(fname)
    return header[param]

def getHeaderComment(fname, param):
    header = getHeader(fname)
    return header.comments[param]

def imageTypeIs(fname, obj):
    return getHeaderValue(fname, "IMAGETYP") == obj

def getImageData(fname):
    hdus = fits.open(fname)
    data = hdus[0].data
    hdus.close()
    return data

def isLight(file):
    if getHeaderValue(file, "IMAGETYP") == "Light Frame":
        return True
    else:
        return False

def isBias(file):
    if getHeaderValue(file, "IMAGETYP") == "Bias Frame":
        return True
    else:
        return False

def isDark(file):
    if getHeaderValue(file, "IMAGETYP") == "Dark Frame":
        return True
    else:
        return False

def isFlat(file):
    if getHeaderValue(file, "IMAGETYP") == "Flat Field":
        return True
    else:
        return False
