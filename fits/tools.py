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

def roundAndCorrect(matrix):
    new_matrix = list()
    for line in matrix:
        new_line = list()
        for value in line:

            if value < 0:
                value = 0

            import numpy

            value = numpy.int16(round(value))



            new_line.append(value)
        new_matrix.append(new_line)
    return new_matrix


def brightness(datas, num):
    values = list()

    for key in datas.keys():
        values.append(float(datas[key].apCounts[6]))
    values = sorted(values, reverse=True)

    result = list()
    for value in values:
        if len(result) < num:
            for key in datas.keys():
                if float(datas[key].apCounts[6]) == value:
                    result.append(datas[key])

    return result

def calculateMove(actual, new):
    #  ( despl x, despl y)
    numberOfDistancesMatch = 3
    maxPixelsVariation = 3

    result = (0, 0, False)
    matchStars = list()
    for data in actual:
        distances = destances(data, actual)
        for nData in new:
            ndistances = destances(nData, new)
            match = 0
            for distance in distances:
                for ndistance in ndistances:
                    if (abs(float(distance[0]) - float(ndistance[0])) < maxPixelsVariation) and (abs(float(distance[1]) - float(ndistance[1])) < maxPixelsVariation):
                        match += 1

            if match > numberOfDistancesMatch:
                matchStars.append((data, nData))

    if len(matchStars) == 0:
        #for data in actual:
        #    print(destances(data, actual))
        #print("===========================================")
        #print("===========================================")
        #print("===========================================")
        #for nData in new:
        #    print(destances(nData, new))
        print("No stars match!!! ")
        return None

    xMove = 0
    yMove = 0
    for match in matchStars:
        xMove += float(match[0].x) - float(match[1].x)
        yMove += float(match[0].y) - float(match[1].y)
    xMove = xMove / len(matchStars)
    yMove = yMove / len(matchStars)

    return (xMove, yMove)




def destances(data, datas):
    result = list()
    for dat in datas:
        if data.x != dat.x and data.y != dat.y:
            result.append((float(data.x) - float(dat.x), float(data.y) - float(dat.y)))
    return result


def separateByTarget(fits):
    for fit in fits:
        getHeaderValue(fit, "OBJECT")
        #TODO: falta acavar
