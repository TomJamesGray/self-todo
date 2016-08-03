import oursql
import os
import logging
import sys
import getpass
from src.api import Api
from src.helpers import getConfPart
class Client():
    def __init__(self):
        __host = getConfPart("db","host")
        __user = getConfPart("db","user")
        __password = getConfPart("db","password")
        __dbName = getConfPart("db","dbName")
        self.api = Api(__host,__user,__password,__dbName)
        self.userId = None
        
    def createListPrompt(self):
        listName = input("create > ")
        #Check if that list name is unique
        try:
            namesOfExistingLists = self.api.getLists(self.userId,["listName"])
        except ValueError as e:
            print(e)
            return False
        if (listName,) in namesOfExistingLists:
            print("List name already exists")
            return False

        self.api.createList(listName,self.userId)    

    def addListItemPrompt(self):
        listToAddTo = input("add - list name > ")
        itemContents = input("add - item > ")
        listId = self.api.getListId(listToAddTo)

        #Last arg (0) is to say this item hasn't been completed
        self.api.saveListItem(listId,itemContents,0)
    
    #Print all the lists in the db
    def listListsPrompt(self):
        try:
            listNames = self.api.getLists(self.userId,["listName"])
        except ValueError as e:
            print(e)
            return False

        for i in range(0,len(listNames)):
            print("{}: {}".format(i,listNames[i][0]))

    def listItemsPrompt(self):
        listName = input("todos - list name > ")
        listId = self.api.getListId(listName)
        listItems = self.api.getListItems(listId,["content","completed"])
        for i in range(0,len(listItems)):
            completed = ""
            if listItems[i][1] == 1:
                completed = "✓"
            elif listItems[i][1] == 0:
                completed = "X"
            print("{}: {} {}".format(i,completed,listItems[i][0]))
  

    def removeListItemPrompt(self):
        listName = input("rmt - listName > ")
        listId = self.api.getListId(listName)
        listItems = self.api.getListItems(listId,["todoId"])
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
    
    def markListItemPrompt(self):
        listName = input("mark - list name > ")
        listId = self.api.getListId(listName)
        listItems = self.api.getListItems(listId,["todoId","completed"])
        todoToMark = int(input("mark - todo number > "))
        if todoToMark >=len(listItems):
            print("todo number is out of range")
            return False
        else:
            if listItems[todoToMark][1] == 0:
                self.api.markListItem(listItems[todoToMark][0],1)
            else:
                self.api.markListItem(listItems[todoToMark][0],0)

    def showHelp(self):
        f = open(os.path.abspath('src/help.txt'),'r')
        print(f.read())
        f.close()

    def runIt(self):
        client = Client()
        choices = {
            'add':self.addListItemPrompt,
            'create':self.createListPrompt,
            'lists':self.listListsPrompt,
            'todos':self.listItemsPrompt,
            'rmt':self.removeListItemPrompt,
            'rml':self.removeListPrompt,
            'mark':self.markListItemPrompt,
            'help':self.showHelp
        }
        #Log user in
        userName = input("User name > ")
        password = getpass.getpass("Password > ")
        if self.api.validateUser(self.userName,password):
            self.userId = self.api.getUserId(self.userName)
            while True:
                try:
                    decision = input("> ")
                    try:
                        func = choices.get(decision,self.runIt)
                        func()
                    except ValueError as e:
                        print("Value error occued {}".format(e))
                except KeyboardInterrupt:
                        sys.exit(1)
        else:
            print("Authentication failed")

