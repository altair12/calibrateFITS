# -*- coding: utf-8 -*-
__author__ = 'fgh'


import commands
import os
import shutil
import glob
import ntpath

from beans.Data import Data
from beans.Image import Image
from beans.Star import Star

from fits.tools import brightness
from fits.tools import calculateMove

from astropy.io import fits
from fits.tools import getHeader
from fits.tools import getImageData


# tool to find stars:
# http://munipack.physics.muni.cz/guide.html
# how to install it

# grafiques
# http://graphite.wikidot.com/


images = list()

# /home/fgh/compartida/20150127/HAT-P-20b_R_000050084.FIT
inputPath = "/home/fgh/compartida/20150127/"
tmpPath = "/tmp/"

allFitsFiles = glob.glob(os.path.join(inputPath, "*.FIT"))
allFitsFiles.sort()

#TODO: diferenciar tarhgets diferents!!!

for file in allFitsFiles:
    print("Finding stars in " + file)

    #bkp file
    tmpFile = os.path.join(tmpPath,ntpath.basename(file))
    shutil.copyfile(file, tmpFile)

    # find stars and calculate brigness
    os.system("munipack find -f 2 -th 8 " + tmpFile)
    os.system("munipack aphot " + tmpFile)

    apTable = commands.getoutput("munipack -lt fits " + tmpFile + "[2]")
    julianDateGeocentric = commands.getoutput("munipack fits -K JD " + tmpFile).split()[2]

    image = Image(tmpFile, julianDateGeocentric)

    lines = apTable.split("\n")
    for line in lines:
        values = line.split()
        data = Data(values[0], values[1], values[2], values[3], julianDateGeocentric)
        data.addCount(values[4], values[5], 1)
        data.addCount(values[6], values[7], 2)
        data.addCount(values[8], values[9], 3)
        data.addCount(values[10], values[11], 4)
        data.addCount(values[12], values[13], 5)
        data.addCount(values[14], values[15], 6)
        data.addCount(values[16], values[17], 7)
        data.addCount(values[18], values[19], 8)
        data.addCount(values[20], values[21], 9)
        data.addCount(values[22], values[23], 10)
        data.addCount(values[24], values[25], 11)
        data.addCount(values[26], values[27], 12)

        image.addData(values[0], values[1], data)

    images.append(image)
    os.remove(tmpFile)




numStarsToLacate = 6
stars = list()
actual = list()
new = list()
iteration = 0
for ima in images:
    if len(stars) == 0:
        for data in ima.dates.values():
            star = Star()
            star.addData(data)
            stars.append(star)
        actual = brightness(ima.dates, numStarsToLacate)
    else:
        new = brightness(ima.dates, numStarsToLacate)

        # calcular distancia entre estrelles de la imatge
        move = calculateMove(actual, new)

        print(str(move) + " --> " + ima.name)

        if move is not None:
            # try to add stars data
            for data in ima.dates.values():
                minDis = 999
                minDisStar = None
                for star in stars:
                    starData = star.getLastData()

                    newX = float(starData.x) - move[0]
                    newY = float(starData.y) - move[1]

                    if abs(float(data.x)-newX) < 1 and abs(float(data.y)-newY) < 1:
                        dis = abs(float(data.x)-newX) + abs(float(data.y)-newY)
                        if dis < minDis:
                            minDis = dis
                            minDisStar = star

                if minDisStar is None:
                    star = Star()
                    star.addData(data)
                    stars.append(star)
                else:
                    minDisStar.addData(data)

            actual = new
        else:
            print("No stars Matched in " + ima.name)


for star in stars:
    datesJD = list()
    for data in star.datas:
        if data.date in datesJD:
            for repdata in star.datas:
                 if data.date == repdata.date:
                     print(repdata.x + "," + repdata.y + " = " + repdata.apCounts[2] + " -- " + repdata.date)
            print("---------------------------------")
        else:
            datesJD.append(data.date)


print("Estrelles: "+ str(len(stars)))







dataFit = getImageData("/home/fgh/compartida/20150127/HAT-P-20b_R_000050074.FIT")
#dataFitTT = getImageData("/tmp/HAT-P-20b_R_000050090.FIT")




for line in dataFit:
    for value in line:
        value = 0


for star in stars:
    if len(star.datas) == 1:
        for data in star.datas:
            for i in range(0, 10):
                if round(float(data.y))+i < 1024 and round(float(data.x)) < 1024:
                    dataFit[round(float(data.y))+i][round(float(data.x))] = 65500


#dataFit += dataFitTT
hdr = getHeader(allFitsFiles[0])
fits.writeto("/tmp/test.fits", dataFit, header=hdr, clobber=True)


quantitats = dict()
for star in stars:
    if len(star.datas) not in quantitats.keys():
        quantitats[len(star.datas)] = 1
    else:
        quantitats[len(star.datas)] += 1

for key in quantitats.keys():
    print("[" + str(key) + "] = " + str(quantitats[key]))


