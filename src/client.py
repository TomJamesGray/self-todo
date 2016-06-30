import oursql
import os
import logging
from configparser import SafeConfigParser
from src.api import Api
class Client():
    def __init__(self):
        __host = self.getConfPart("db","host")
        __user = self.getConfPart("db","user")
        __password = self.getConfPart("db","password")
        __dbName = self.getConfPart("db","dbName")
        self.api = Api(__host,__user,__password,__dbName)
       
    def getConfPart(self,section,key):
        parser = SafeConfigParser()
        #Get absolute dir for config file
        configLocation = os.path.abspath("config.ini")
        parser.read(configLocation)
        return parser.get(section,key)
    
    def createListPrompt(self):
        listName = input("create > ")
        #Check if that list name is unique
        try:
            namesOfExistingLists = self.api.getLists("listName")
        except ValueError as e:
            print(e)
            return False
        if (listName,) in namesOfExistingLists:
            print("List name already exists")
            return False

        self.api.createList(listName)    

    def addListItemPrompt(self):
        listToAddTo = input("add - list name > ")
        itemContents = input("add - item > ")
        listId = self.api.getListId(listToAddTo)

        #Last arg (0) is to say this item hasn't been completed
        self.api.saveListItem(listId,itemContents,0)
    
    #Print all the lists in the db
    def listListsPrompt(self):
        try:
            listNames = self.api.getLists('listName')
        except ValueError as e:
            print(e)
            return False

        for i in range(0,len(listNames)):
            print("{}: {}".format(i,listNames[i][0]))

    def listItemsPrompt(self):
        listName = input("list name")
        logging.info("list name is {}".format(listName))

        listItems = self.api.getListItems(self.api.getListId(listName),"content")

        print(listItems)

    def removeListItemPrompt(self):
        listName = input("rmt - listName > ")
        listIdFromName = self.api.getListId(listName)
        listItems = self.api.getListItems(listId,"todoId")
        todoToRemove = int(input("rmt - todo number > "))

        if todoToRemove >= len(listItems):
            print("todo number is out of range")
            return False
        else:
            self.api.removeListItem(listItems[todoToRemove][0])
            
    def removeListPrompt(self):
       listName = input("rml - list name > ")
       listId = self.api.getListId(listName)
       self.api.removeList(listId)

    def showHelp(self):
        f = open(os.path.abspath('src/help.txt'),'r')
        print(f.read())
        f.close()
