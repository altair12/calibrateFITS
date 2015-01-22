
__author__ = 'fgh'


# Initial file to start all the proces,
# at the begining this script include parts that then it will be moved to other parts


# REFERENCES:
# https://github.com/shkw0k/cookbook/tree/master/
#        pip install "ipython[notebook]"        paquet que permet visualitzar
# iniciem amb: ipython notebook --pylab inline


from astropy.io import fits
import glob


def getHeader (fname):
    hdus = fits.open(fname)
    header = hdus[0].header
    hdus.close()
    return header

def imageTypeIs(fname, obj):
    header = getHeader(fname)
    return header["IMAGETYP"] == obj

def getImageData (fname):
    print(fname)
    hdus = fits.open(fname)
    data = hdus[0].data
    hdus.close()
    return data

def avgFits (fitsFiles):
    curr = getImageData(fitsFiles[0])
    for f in fitsFiles[1:]:
        curr = curr + getImageData(f)
    curr = curr / len (fitsFiles)
    return curr

def substractFits(original, subtracted):
    curr = getImageData(original) - getImageData(subtracted)
    return curr

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