# -*- coding: utf-8 -*-
__author__ = 'fgh'


# Initial file to start all the proces,
# at the begining this script include parts that then it will be moved to other parts


# REFERENCES:
# https://github.com/shkw0k/cookbook/tree/master/
#        pip install "ipython[notebook]"        paquet que permet visualitzar
# iniciem amb: ipython notebook --pylab inline
#
#
# Folow this image acllibrations
# http://nbviewer.ipython.org/gist/mwcraig/06060d789cc298bbb08e


import glob
import os
import shutil
import ntpath
import numpy

from datetime import timedelta
from datetime import datetime
from astropy.io import fits

from fits.tools import getHeader
from fits.tools import getHeaderValue
from fits.tools import isLight
from fits.tools import isBias
from fits.tools import isDark
from fits.tools import isFlat
from fits.tools import getImageData
from fits.tools import roundAndCorrect
from fits.operations import discardBadImages
from fits.operations import medianFits
from fits.operations import discardWrongTemperatureImages
from fits.operations import getCloserMaster
from fits.operations import separateFitsByFilter
from utils.system import ensureExist



inputPath = "/home/fgh/Dropbox/nit/"
outputPath = "/home/fgh/compartida/Astronomia/"

# The destination directory structure will be
originalImagesPath = os.path.join(outputPath, "originals/images/")                          # path of the original images separated by observation nights
originalCalibrationImagesPath = os.path.join(outputPath, "originals/callibration/")         # path of the original calibration images separated by observation nights
calibratedImagePath = os.path.join(outputPath, "calibrated/images/")
calibratedCalibrationImagesPath = os.path.join(outputPath, "calibrated/callibration/")

def createStructure():
    # Ensure all structure Exist and create if it don't exist
    ensureExist(originalImagesPath)
    ensureExist(originalCalibrationImagesPath)
    ensureExist(calibratedImagePath)
    ensureExist(calibratedCalibrationImagesPath)

def orderImages():
    # First move the images to another folder separating it by calibration and images
    allFitsFiles = glob.glob(os.path.join(inputPath, "*.FIT"))

    for file in allFitsFiles:
        # First detect if file is image or calibration image
        destinationPath = None
        if isLight(file):
            destinationPath = originalImagesPath
        else:
            destinationPath = originalCalibrationImagesPath

        # Calculate subpath (the name is the date night of the observation)
        fitsDate = datetime.strptime(getHeaderValue(file, "DATE-OBS"), "%Y-%m-%dT%H:%M:%S")
        subPathName = fitsDate.strftime("%Y%m%d")
        if int(fitsDate.strftime("%H")) < 12:
            subPathName = (fitsDate - timedelta(days=1)).strftime("%Y%m%d")

        # Create subpath if is need
        destinationPath = os.path.join(destinationPath, subPathName)
        if not os.path.exists(destinationPath):
            os.makedirs(destinationPath)

        # move file
        shutil.move(file, os.path.join(destinationPath,ntpath.basename(file)))


def generateMasterBias():
    # Generate calibration Masters BIAS
    for dir in os.listdir(originalCalibrationImagesPath):
        dirPath = os.path.join(originalCalibrationImagesPath,dir)
        if os.path.isdir(dirPath):
            biasFiles = list()

            for file in os.listdir(dirPath):
                filePath = os.path.join(originalCalibrationImagesPath,dir, file)
                if isBias(filePath):
                    biasFiles.append(filePath)
            if len(biasFiles) > 0:
                masterPath = os.path.join(calibratedCalibrationImagesPath,dir,"MASTER_BIAS.FIT")
                if not os.path.exists(masterPath):
                    ensureExist(os.path.join(calibratedCalibrationImagesPath,dir))

                    discardWrongTemperatureImages(biasFiles)
                    biasFiles = discardBadImages(biasFiles)

                    if len(biasFiles) > 10:
                        avgBias = medianFits(biasFiles)
                        hdr = getHeader(biasFiles[0])
                        fits.writeto(masterPath, avgBias, header=hdr, clobber=True)
                        print("Master bias saved: " + masterPath)
                    else:
                        print("Not many files to calculate Master Bias of " + dirPath)

def generateMasterDarks():
    # Generate calibration Masters DARKS
    for dir in os.listdir(originalCalibrationImagesPath):
        dirPath = os.path.join(originalCalibrationImagesPath,dir)
        if os.path.isdir(dirPath):
            darkFiles = list()

            for file in os.listdir(dirPath):
                filePath = os.path.join(originalCalibrationImagesPath, dir, file)
                if isDark(filePath):
                    darkFiles.append(filePath)
            if len(darkFiles) > 0:
                masterPath = os.path.join(calibratedCalibrationImagesPath,dir,"MASTER_DARK.FIT")
                if not os.path.exists(masterPath):
                    ensureExist(os.path.join(calibratedCalibrationImagesPath,dir))

                    discardWrongTemperatureImages(darkFiles)
                    darkFiles = discardBadImages(darkFiles)

                    if len(darkFiles) > 10:
                        avgDirtyDark = medianFits(darkFiles)

                        masterBias = getCloserMaster("BIAS", dir, calibratedCalibrationImagesPath, None)
                        avgDark = avgDirtyDark - getImageData(masterBias)

                        hdr = getHeader(darkFiles[0])
                        fits.writeto(masterPath, avgDark, header=hdr, clobber=True)
                        print("Master Dark saved: " + masterPath)
                    else:
                        print("Not many files to calculate Master Bias of " + dirPath)

def generateMasterFlats():
    # Generate calibration Masters FLAT
    for dir in os.listdir(originalCalibrationImagesPath):
        dirPath = os.path.join(originalCalibrationImagesPath,dir)
        if os.path.isdir(dirPath):
            flatFiles = list()

            for file in os.listdir(dirPath):
                filePath = os.path.join(originalCalibrationImagesPath, dir, file)
                if isFlat(filePath):
                    flatFiles.append(filePath)
            if len(flatFiles) > 0:
                # Separate from filters
                flatFilesSeparated = separateFitsByFilter(flatFiles)

                for filter in flatFilesSeparated.keys():
                    masterPath = os.path.join(calibratedCalibrationImagesPath, dir, "MASTER_FLAT_" + filter + ".FIT")
                    if not os.path.exists(masterPath):
                        ensureExist(os.path.join(calibratedCalibrationImagesPath,dir))

                        discardWrongTemperatureImages(flatFiles)
                        flatFiles = discardBadImages(flatFiles)

                        if len(flatFiles) > 10:
                            masterBias = getCloserMaster("BIAS", dir, calibratedCalibrationImagesPath, None)
                            masterDark = getCloserMaster("DARK", dir, calibratedCalibrationImagesPath, None)

                            avgFlat = []
                            for flat in flatFiles:
                                dataFlat = getImageData(flat)
                                dataFlat = dataFlat - getImageData(masterBias)
                                dataFlat = dataFlat - getImageData(masterDark) * getHeaderValue(flat, "EXPTIME")/ getHeaderValue(masterDark, "EXPTIME")
                                # normalize
                                dataFlat = dataFlat / numpy.mean(dataFlat)

                                avgFlat.append(dataFlat)
                            masterFlatData = numpy.median(avgFlat, axis=0)

                            hdr = getHeader(flatFiles[0])
                            fits.writeto(masterPath, masterFlatData, header=hdr, clobber=True)
                            print("Master Flat saved: " + masterPath)
                        else:
                            print("Not many files to calculate Master Flat of " + dirPath)



def calibrateImages():
    for dir in os.listdir(originalImagesPath):
        dirPath = os.path.join(originalImagesPath,dir)
        if os.path.isdir(dirPath):
            for file in os.listdir(dirPath):
                filePath = os.path.join(originalImagesPath, dir, file)
                destFilePath = os.path.join(calibratedImagePath, dir, file)

                if isLight(filePath) and not os.path.exists(destFilePath):
                    ensureExist(os.path.join(calibratedImagePath, dir))

                    masterBias = getCloserMaster("BIAS", dir, calibratedCalibrationImagesPath, None)
                    masterDark = getCloserMaster("DARK", dir, calibratedCalibrationImagesPath, None)
                    masterFlat = getCloserMaster("FLAT", dir, calibratedCalibrationImagesPath, getHeaderValue(filePath, "FILTER"))

                    dataFit = getImageData(filePath)
                    dataFit = dataFit - getImageData(masterBias)
                    dataFit = dataFit - getImageData(masterDark) * getHeaderValue(filePath, "EXPTIME")/ getHeaderValue(masterDark, "EXPTIME")
                    dataFit = dataFit / getImageData(masterFlat)
                    dataFit = roundAndCorrect(dataFit)

                    fliped = ""
                    # To prevent meridian flip, set WEST as default meridian and flip EAST (param PIERSIDE of the header)
                    if getHeaderValue(filePath, "PIERSIDE") == "EAST":
                        dataFit = numpy.rot90(dataFit, 2)
                        fliped = " flipped."

                    hdr = getHeader(filePath)
                    fits.writeto(destFilePath, dataFit, header=hdr, clobber=True)
                    print("Image saved: " + destFilePath + fliped)




def main():
    createStructure()
    orderImages()

    generateMasterBias()
    generateMasterDarks()
    generateMasterFlats()
    calibrateImages()


if __name__ == '__main__':
    main()


#       https://github.com/vterron/lemon



