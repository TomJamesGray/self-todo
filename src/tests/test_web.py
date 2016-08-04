import pytest
import requests
import src.main
#Import client module only to connect to db
#from config values
from src.client import Client
"""
Create three users, one admin through api module
then create one admin, one regular user logged in as the
original admin user
"""
users = [
    {
        'userName':'sudo',
        'password':'sudo'
    },
    {
        'userName':'assistant',
        'password':'assistant'
    },
    {
        'userName':'slave',
        'password':'slave'
    }
]
@pytest.fixture(scope="module")
def makeSudo(request):
    global users
    client = Client()
    api = client.api
    api.createUser(users[0]['userName'],users[0]['password'],'admin')
    users[0]['userId'] = api.getUserId(users[0]['userName'])
    def teardown():
        api.deleteUser(users[0]['userId'])
    request.addfinalizer(teardown)
    return api

def testLoginSudo(makeSudo):
    global users
    r = requests.post('http://localhost:5000/login',data=users[0])
    assert r.status_code == requests.codes.ok
