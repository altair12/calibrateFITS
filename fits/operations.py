# -*- coding: utf-8 -*-
__author__ = 'fgh'

import os
import numpy

from collections import Counter
from datetime import date, datetime

from tools import getImageData
from tools import getHeaderValue

#def avgFits(fitsFiles):
#    curr = getImageData(fitsFiles[0])
#    for f in fitsFiles[1:]:
#        curr = curr + getImageData(f)
#    curr = curr / len (fitsFiles)
#    return curr

def medianFits(fitsFiles):
    result_concat = []
    for f in fitsFiles:
        result_concat.append(getImageData(f))
    return numpy.median(result_concat, axis=0)



def substractFits(original, subtracted):
    curr = getImageData(original) - getImageData(subtracted)
    return curr


def discardBadImages(images):
    # avgFlats is the average of the biases
    avgFlats = medianFits(images)

    # substract average from first image
    for image in images:
        substract = getImageData(image) - avgFlats

        num = 0
        for line in substract:
            for value in line:
                if abs(value) > 1000:
                    num += abs(value)

        if num > 20000:
            print image + " is too diferent than the average: " + str(num)
            images.remove(image)
    return images

def discardWrongTemperatureImages(images):
    tempList = list()
    for image in images:
        tempList.append(getHeaderValue(image, "CCD-TEMP"))

    data = Counter(tempList)
    temp = data.most_common(1)[0][0]

    for image in images:
        imageTemp = getHeaderValue(image, "CCD-TEMP")
        if abs(imageTemp - temp) > 1:
            print("Discard image "+ image + " because have a wrong temperature "+ str(imageTemp) + " respect " + str(temp))


def getCloserMaster(masterType, masterDir, calibratedCalibrationImagesPath, filter):
    result = None
    #First look in the same folder
    if filter is None:
        masterName = "MASTER_" + masterType +".FIT"
    else:
        masterName = "MASTER_" + masterType + "_" + filter +".FIT"
    result = os.path.join(calibratedCalibrationImagesPath,masterDir, masterName)
    if not os.path.exists(result):
        masterList = {}
        for dir in os.listdir(calibratedCalibrationImagesPath):
            if os.path.exists(os.path.join(calibratedCalibrationImagesPath,dir, masterName)):
                masterList[dir] = abs((datetime.strptime(masterDir, "%Y%m%d") - datetime.strptime(dir, "%Y%m%d")).days)
        minimum = min(masterList.values())
        for key in masterList.keys():
            if masterList[key] == minimum:
                result = os.path.join(calibratedCalibrationImagesPath,key, masterName)
    return result


def separateFitsByFilter(flats):
    result = {}
    for flat in flats:
        filter = getHeaderValue(flat, "FILTER")
        if not result.has_key(filter):
            result[filter] = list()
        result[filter].append(flat)
    return result