from configparser import SafeConfigParser
from src.client import Client 
import pytest
@pytest.fixture
def makeList(request):
    client = Client()
    client.api.createList("pyTestList")
    listId = client.api.getListId("pyTestList")
    
    def removeList():
        client.api.removeList(listId)
        client.api.closeConnection()
    request.addfinalizer(removeList)
    return client.api

def testListIsPresent(makeList):
    if ("pyTestList",) in makeList.getLists("listName"):
        assert True
    else:
        assert False
