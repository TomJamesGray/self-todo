import oursql
from src.api import Api
class Client():
    def __init__(self,conn):
        self.api = Api(conn)

    def createListPrompt(self):
        listName = input("create > ")
        self.api.createList(listName)    

    def addListItem(self):
        print("Adding list item")
