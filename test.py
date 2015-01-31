__author__ = 'fgh'

import glob
import os
import shutil
import ntpath

from datetime import timedelta
from datetime import datetime

from fits.tools import *

from fits.tools import getHeaderValue



#substract = getImageData("/home/fgh/compartida/Astronomia/HAT-P-20b_R_000050075___1.FIT") - getImageData("/home/fgh/compartida/Astronomia/HAT-P-20b_R_000050075___2.FIT")
#substract = getImageData("/home/fgh/compartida/Astronomia/HAT-P-20b_R_000050075___2.FIT")
#substract = getImageData("/home/fgh/compartida/Astronomia/calibrated/callibration/20150127/MASTER_DARK.FIT")

#substract = getImageData("/home/fgh/compartida/Astronomia/originals/images/20150127/HAT-P-20b_R_000050075.FIT")
#substract = getImageData("/home/fgh/compartida/Calibration Frames.fit")
substract = getImageData("/home/fgh/compartida/Astronomia/calibrated/callibration/20150127/MASTER_FLAT_R.FIT")
num = 0
for line in substract:
    for value in line:
        if value != 0:
            print(value)
            num += 1

print("----------------------")
print(num)