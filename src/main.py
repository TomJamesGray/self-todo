#!/usr/bin/env python3
from flask import Flask
from src.api import Api

app = Flask(__name__)
api = Api('192.168.1.2','example','password','self_todo')

@app.route('/')
def index():
    return str(api.getLists(['listName']))

@app.route('/list/<listName>')
def show_todos(listName):
    return str(api.getListItems(api.getListId(listName),'content,completed'))

