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

    #Get list id by list name
    #returned as tuple
    def getListId(self,listName):
        self.cursor.execute("SELECT listId FROM todoLists where listName=?",(listName,))
        return self.cursor.fetchone()

    def saveListItem(self,listId,content,completed):
        self.cursor.execute("INSERT INTO todos (listId,content,completed) \
                VALUES (?,?,?)",(listId,content,completed))