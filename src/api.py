import oursql
class Api(object):
    def __init__(self,conn):
        self.conn = conn
        self.cursor = self.conn.cursor(oursql.DictCursor)
    def createList(self,listName):
        self.cursor.execute("INSERT INTO todoLists SET listName=?",(listName,))
