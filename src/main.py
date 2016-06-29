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

def main():
    client = Client()
    choices = {
        'add':client.addListItemPrompt,
        'create':client.createListPrompt,
        'lists':client.listLists,
        'todos':client.listItems
    }
    while True:
        decision = input("> ")
        try:
            func = choices.get(decision,)
            func()
        except TypeError:
            print("Unknown command: {}".format(func))

