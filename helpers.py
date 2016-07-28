import os
from configparser import SafeConfigParser

def getConfPart(section,key):
    parser = SafeConfigParser()
    location = os.path.abspath("config.ini")
    parser.read(location)
    return parser.get(section,key)
