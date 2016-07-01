#Connect to db
from configparser import SafeConfigParser
from src.client import Client
import os
import oursql
import sys

def main():
    client = Client()
    choices = {
        'add':client.addListItemPrompt,
        'create':client.createListPrompt,
        'lists':client.listListsPrompt,
        'todos':client.listItemsPrompt,
        'rmt':client.removeListItemPrompt,
        'rml':client.removeListPrompt,
        'mark':client.markListItemPrompt,
        'help':client.showHelp
    }
    while True:
        try:
            decision = input("> ")
            try:
                func = choices.get(decision,main)
                func()
            except ValueError as e:
                print("Value error occued {}".format(e))
        except KeyboardInterrupt:
            sys.exit(1)

