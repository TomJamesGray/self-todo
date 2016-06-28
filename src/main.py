#Connect to db
from configparser import SafeConfigParser
from src.client import Client
import os
import oursql

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
    
    db = oursql.connect(host=host,user=user,
            passwd=password,db=dbName)
    
    return db

def main():
    conn = setup()
    client = Client(conn)
    choices = {
        'add':client.addListItem,
        'create':client.createListPrompt
    }
    while True:
        decision = input("> ")
        func = choices.get(decision)
        func()

