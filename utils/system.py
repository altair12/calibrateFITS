__author__ = 'fgh'

import os

# Ensure that all directory's in the path exist,
# create it if it don't exist
def ensureExist(path):
    if path is None or path == "":
        raise Exception("[utils.system.ensureExist ERROR] path param must not be None or empty!")
    if not os.path.exists(path):
        os.makedirs(path)