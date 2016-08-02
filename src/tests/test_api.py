from configparser import SafeConfigParser
from src.client import Client 
import pytest
listName = "pyTestList"
listId = None
todoId = None
userId = None
todoContents = "todo content"
userName = "travis"
userPassword = "password"
@pytest.fixture(scope="module")
def makeList(request):
    global listName,listId,todoContents,userId,userName,userPassword
    client = Client()
    client.api.createUser(userName,userPassword)
    userId = client.api.getUserId("travis")
    client.api.createList("pyTestList",userId)
    listId = client.api.getListId("pyTestList")
    client.api.saveListItem(listId,todoContents,0)
    def removeList():
        #Remove todo first to stop foreign key error
        client.api.removeListItem(todoId[0][0])
        client.api.removeList(listId)
        client.api.deleteUser(userId)
        client.api.closeConnection()
    request.addfinalizer(removeList)
    return client.api

def testListIsPresent(makeList):
    global listName,userId
    print(userId)
    if ("pyTestList",) in makeList.getLists(userId,["listName"]):
        assert True
    else:
        assert False

def testGetTodoId(makeList):
    global todoContents,listId,todoId
    todoId = makeList.getTodoId(todoContents,listId)
    if len(todoId) == 1:
        assert True
    else:
        assert False

def testUserIsValid(makeList):
    global userId
    assert makeList.isUser(userId)

def testValidateUser(makeList):
    global userId,userName,userPassword
    assert makeList.validateUser(userName,userPassword)

def testValidateUnkwownUser(makeList):
    assert not makeList.validateUser('notAUser','pass')

def testValidateUserWrongPassword(makeList):
    global userName
    assert not makeList.validateUser(userName,'a')
