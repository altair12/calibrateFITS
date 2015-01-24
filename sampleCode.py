
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


from astropy.io import fits
import glob

from fits.tools import imageTypeIs
from fits.tools import getHeader
from fits.operations import avgFits
from fits.operations import substractFits



AllFitsFiles = glob.glob("/home/fgh/Astronomia/flats/R*.FIT")
Flats = [ f for f in AllFitsFiles if imageTypeIs(f, "Flat Field") ]

# avgFlats is the average of the biases
avgFlats = avgFits(Flats)

hdr = getHeader(Flats[0])
masterFlats = "/home/fgh/Astronomia/flats/masterFlats.fits"
fits.writeto(masterFlats, avgFlats, header=hdr, clobber=True)

# substract average from first image
substract = substractFits(Flats[0], masterFlats)

hdr = getHeader(Flats[0])
substractFlats = "/home/fgh/Astronomia/flats/substract.fits"
fits.writeto(substractFlats, substract, header=hdr, clobber=True)


# substract average from first image
for flat in Flats:
    substract = substractFits(flat, masterFlats)

    num = 0
    for line in substract:
        for value in line:
            if abs(value) > 1000:
                num += abs(value)

    if num > 10000:
        print flat + " Te mes de 10 pixels fora de la mitja, te: " + str(num)