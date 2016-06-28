import oursql
from src.api import Api
class Client():
    def __init__(self,conn):
        self.api = Api(conn)

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

    def addListItem(self):
        print("Adding list item")
