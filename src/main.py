#Connect to db
from configparser import SafeConfigParser
from src.client import Client
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
    
    db = _mysql.connect(host,user,
            password,dbName)
    
    return db

def main():
    conn = setup()
    client = Client(conn)
    choices = {
        'add':client.addListItem
    }
    while True:
        decision = input("> ")
        func = choices.get(decision)
        func()

