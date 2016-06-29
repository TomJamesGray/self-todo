import oursql
class Api(object):
    def __init__(self,host,user,password,dbName):
        self.conn = oursql.connect(host=host,user=user,
                passwd=password,db=dbName)
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

    def saveListItem(self,listId,content,completed):
        self.cursor.execute("INSERT INTO todos (listId,content,completed) \
                VALUES (?,?,?)",(listId,content,completed))

    #Get list id by list name
    #returned as int 
    def getListId(self,listName):
        self.cursor.execute("SELECT listId FROM todoLists where listName=?",(listName,))
        return self.cursor.fetchone()[0]

    def getListItems(self,listId,columns):
        columnNames = ['todoId','listId','content','completed']
        columnsList = columns.split(",")

        for column in columnsList:
            if column not in columnNames:
                raise ValueError("Column name provided is not in column names")
        
        self.cursor.execute("SELECT {} FROM todos WHERE listId=?".format(columns),(listId,))
        return self.cursor.fetchall()
    
    #Remove the item from the list based off the todoId
    def removeListItem(self,todoId):
        self.cursor.execute("DELETE FROM todos WHERE todoId=?",(todoId,))

    def removeList(self,listId):
        self.cursor.execute("DELETE FROM todoLists WHERE listId=?",(listId,))
