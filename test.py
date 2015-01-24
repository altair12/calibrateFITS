__author__ = 'fgh'

import glob
import os
import shutil
import ntpath

from datetime import timedelta
from datetime import datetime

from fits.tools import getHeaderValue

print(getHeaderValue("/home/fgh/compartida/Astronomia/originals/callibration/20141209/BI_000044088.FIT", "IMAGETYP"))