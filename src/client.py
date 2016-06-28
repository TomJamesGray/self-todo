import oursql
class Client(object):
    def __init__(self,conn):
        self.conn = conn
        self.cursor = self.conn.cursor(oursql.DictCursor)

    def createList(self):
        listName = input("create > ")
        
        self.cursor.execute("INSERT INTO todoLists SET listName=?",(listName,))
    def addListItem(self):
        print("Adding list item")
