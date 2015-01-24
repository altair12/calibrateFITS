
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

from datetime import timedelta
from datetime import datetime

from fits.tools import getHeader
from fits.tools import getHeaderValue
from fits.tools import isLight
from fits.tools import isBias
from fits.operations import discardImages



# Some initial variables
#inputPath = "/home/fgh/Astronomia/input/*.FIT"
#originalImagesPath = "/home/fgh/Astronomia/originals/images/"                           # path of the original images separated by observation nights
#originalCallibrationImagesPath = "/home/fgh/Astronomia/originals/callibration/"         # path of the original calibration images separated by observation nights

inputPath = "/home/fgh/Dropbox/nit/"
originalImagesPath = "/home/fgh/compartida/Astronomia/originals/images/"                           # path of the original images separated by observation nights
originalCalibrationImagesPath = "/home/fgh/compartida/Astronomia/originals/callibration/"         # path of the original calibration images separated by observation nights
calibratedImagePath = "/home/fgh/compartida/Astronomia/calibrated/images/"
calibratedCalibrationImagesPath = "/home/fgh/compartida/Astronomia/calibrated/callibration/"

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


# Generate calibration Masters
# first start with BIAS
for dir in os.listdir(originalCalibrationImagesPath):
    if os.path.isdir(dir):
        biasFiles = list()
        for file in os.listdir(dir):
            if isBias(file):
                biasFiles.append(file)
        if len(biasFiles) > 0:
            #TODO: mirem si existeix ja el BIAS

            #TODO: mirem que totes tinguin la mateixa temperatura

            biasFiles = discardImages(biasFiles)

            #hdr = getHeader(biasFiles[0])
            #masterBiass = "/home/fgh/Astronomia/flats/masterFlats.fits"
            #fits.writeto(masterFlats, avgFlats, header=hdr, clobber=True)





#    IMAGETYP= 'Flat Field'
#    IMAGETYP= 'Light Frame'
#    CCD-TEMP
#    EXPTIME
#    FILTER










