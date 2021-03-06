import oursql
import bcrypt
class Api(object):
    def __init__(self,host,user,password,dbName):
        self.conn = oursql.connect(host=host,user=user,
                passwd=password,db=dbName)
        self.cursor = self.conn.cursor()

    
    def createList(self,listName,userId):
        self.cursor.execute("INSERT INTO todoLists (listName,userId) \
                VALUES (?,?)",(listName,userId))
    
    #Retrieve all columns for lists from db
    #Columns should provided in a list
    def getLists(self,userId,columns=['listName']):
        columnNames = ['listId','listName','creationDate']

        for column in columns:
            if column not in columnNames:
                raise ValueError("Column name desired provided is not in column names")
        stmnt = "SELECT {} FROM todoLists WHERE userId=?".format(','.join(columns))
        self.cursor.execute(stmnt,(userId,))
        return self.cursor.fetchall()

    def saveListItem(self,listId,content,completed):
        self.cursor.execute("INSERT INTO todos (listId,content,completed) \
                VALUES (?,?,?)",(listId,content,completed))

    #Get list id by list name
    #returned as int 
    def getListId(self,listName):
        self.cursor.execute("SELECT listId FROM todoLists WHERE listName=?",
            (listName,))
        listId = self.cursor.fetchall()
        if listId != None and len(listId) == 1:
            return listId[0][0]
        else:
            raise ValueError("Couldn't find list id")

    #Can provide content, listId or both, will return all
    #the matching todoIds
    def getTodoId(self,content=None,listId=None):
        stmnt = "SELECT todoId FROM todos WHERE "
        #TODO use an orm? try and make it a little bit more 'elegant'
        if content==None and listId==None:
            raise ValueError("Content and listId both not provided, must \
                    provide one or both")
        elif content != None and listId != None:
            stmnt = stmnt + "content=? AND listId=?"
            vals = (content,listId)
        elif content != None and listId == None:
            stmnt = stmnt + "content=?"
            vals = (content,)
        elif content == None and listId == None:
            stmny = stmnt + "listId=?"
            vals = (listId,)

        self.cursor.execute(stmnt,vals)
        return self.cursor.fetchall()

    def getListItems(self,listId,columns=['content']):
        columnNames = ['todoId','listId','content','completed']

        for column in columns:
            if column not in columnNames:
                raise ValueError("Column name provided is not in column names")
        
        self.cursor.execute("SELECT {} FROM todos WHERE listId=? ORDER BY completed".format(','.join(columns)),(listId,))
        return self.cursor.fetchall()
    
    #Remove the item from the list based off the todoId
    def removeListItem(self,todoId):
        self.cursor.execute("DELETE FROM todos WHERE todoId=?",(todoId,))

    def removeList(self,listId):
        self.cursor.execute("DELETE FROM todoLists WHERE listId=?",(listId,))

    def closeConnection(self):
        self.conn.close()

    def markListItem(self,todoId,completed):
        self.cursor.execute("UPDATE todos SET completed=? WHERE todoId=?",(completed,todoId))
    
    def switchItemCompletion(self,todoId):
        self.cursor.execute("SELECT completed FROM todos WHERE todoId=?",(todoId,))
        curStatus = self.cursor.fetchall()[0][0]
        print("status: {}".format(curStatus))
        print("New status: {}".format(int(not curStatus)))
        #Not status will flip the 0 to 1 or vice versa
        self.markListItem(todoId,(int(not curStatus)))

    def switchTodoPriority(self,todoId1,todoId2):
        self.cursor.execute("SELECT listId,content,completed FROM todos WHERE todoId=? OR todoId=?",
                (todoId1,todoId2))
        todoData = self.cursor.fetchall()
        print(todoData)
        stmnt = "UPDATE todos SET listId=?,content=?,completed=? WHERE todoId=?"
        self.cursor.execute(stmnt,todoData[0] + (todoId2,))
        self.cursor.execute(stmnt,todoData[1] + (todoId1,))

    def createUser(self,userName,password,role="user"):
        #Hash the password with a salt
        hashedPw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        self.cursor.execute("INSERT INTO users (userName,password,role) \
            VALUES (?,?,?)",(userName,hashedPw,role))

    def validateUser(self,userName,password):
        #Get user by userName and compare hashed+salted PWs
        self.cursor.execute("SELECT password FROM users WHERE userName=?",
                (userName,))
        data = self.cursor.fetchall()
        if data == []:
            return False

        __actualPassword = data[0][0].encode('utf8')
        
        if bcrypt.hashpw(password.encode('utf8'),__actualPassword) ==  __actualPassword:
            #User password is valid
            return True
        else:
            return False
    
    def getUserId(self,userName):
        self.cursor.execute("SELECT userId FROM users WHERE userName=?",
                (userName,))
        data = self.cursor.fetchall()
        if data == []:
            return False
        return data[0][0]

    def isUser(self,userId):
        self.cursor.execute("SELECT userId FROM users where userId=?",
                (userId,))
        if not self.cursor.fetchall() == []:
            return True
        else:
            return False

    def deleteUser(self,userId):
        self.cursor.execute("DELETE FROM users WHERE userId=?",(userId,))
        return True

    def getUserRole(self,userId):
        self.cursor.execute("SELECT role FROM users WHERE userId=?",(userId,))
        data = self.cursor.fetchall()
        if data == []:
            #No user found
            return False
        else:
            return data[0][0]
