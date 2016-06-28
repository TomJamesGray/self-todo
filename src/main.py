#Connect to db
from configparser import SafeConfigParser
import os
import _mysql

def getConfPart(section,key):
    parser = SafeConfigParser()
    #Get absolute dir for config file
    configLocation = os.path.abspath("config.ini")
    parser.read(configLocation)
    return parser.get(section,key)

def setup():
    host = getConfPart("db","host")
    user = getConfPart("db","user")
    password = getConfPart("db","password")
    dbName = getConfPart("db","dbName")
    
    print("User is {}\nPassword is {}".format(user,password))

    db = _mysql.connect(host,user,
            password,dbName)


def main():
    setup()
