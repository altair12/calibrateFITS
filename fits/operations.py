__author__ = 'fgh'

from tools import getImageData

def avgFits (fitsFiles):
    curr = getImageData(fitsFiles[0])
    for f in fitsFiles[1:]:
        curr = curr + getImageData(f)
    curr = curr / len (fitsFiles)
    return curr

def substractFits(original, subtracted):
    curr = getImageData(original) - getImageData(subtracted)
    return curr


def discardImages(images):
    # avgFlats is the average of the biases
    avgFlats = avgFits(images)

    # substract average from first image
    for image in images:
        substract = getImageData(image) - avgFlats

        num = 0
        for line in substract:
            for value in line:
                if abs(value) > 1000:
                    num += abs(value)

        if num > 10000:
            print image + " is too diferent than the average: " + str(num)
            images.remove(image)
    return images