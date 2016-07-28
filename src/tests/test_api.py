from configparser import SafeConfigParser
from src.client import Client 
import pytest
listName = "pyTestList"
listId = None
todoId = None
todoContents = "todo content"
@pytest.fixture(scope="module")
def makeList(request):
    global listName,listId,todoContents
    client = Client()
    client.api.createList("pyTestList")
    listId = client.api.getListId("pyTestList")
    client.api.saveListItem(listId,todoContents,0)
    def removeList():
        #Remove todo first to stop foreign key error
        client.api.removeListItem(todoId[0][0])
        client.api.removeList(listId)
        client.api.closeConnection()
    request.addfinalizer(removeList)
    return client.api

def testListIsPresent(makeList):
    global listName
    if ("pyTestList",) in makeList.getLists(["listName"]):
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
