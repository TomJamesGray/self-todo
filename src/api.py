import oursql
class Api(object):
    def __init__(self,conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
    
    def createList(self,listName):
        self.cursor.execute("INSERT INTO todoLists SET listName=?",(listName,))
    
    #Retrieve all columns for lists from db
    #Columns should be comma seperated
    def getLists(self,columns):
        columnNames = ['listId','listName','creationDate']
        columnsList = columns.split(",")

        for column in columnsList:
            if column not in columnNames:
                raise ValueError("Column name desired provided is not in column names")

        self.cursor.execute("SELECT {}  FROM todoLists".format(columns))
        return self.cursor.fetchall()
