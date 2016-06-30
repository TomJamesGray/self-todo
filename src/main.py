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
        'lists':client.listListsPrompt,
        'todos':client.listItemsPrompt,
        'rmt':client.removeListItemPrompt,
        'rml':client.removeListPrompt,
        'help':client.showHelp
    }
    while True:
        decision = input("> ")
        func = choices.get(decision)
        func()

