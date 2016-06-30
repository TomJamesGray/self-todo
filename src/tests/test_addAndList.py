from src.api import Api
def test_addAndList():
    api = Api("192.168.1.2","example","password","self_todo")
    api.getListItems(4,"content,completed")
    api.saveListItem(4,"test",0)
    print(api.getListItems(4,"content,completed"))
    assert False
