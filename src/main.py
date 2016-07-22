#!/usr/bin/env python3
from flask import Flask,render_template
from src.api import Api

app = Flask(__name__)
api = Api('192.168.1.2','example','password','self_todo')

@app.route('/')
def index():
    #Get lists and get the list names out of the tuple
    lists = api.getLists()
    a = []
    for i in lists:
        a.append(i[0])
    return render_template('index.html',lists=a)

@app.route('/list/<listName>')
def show_todos(listName):
    todos = api.getListItems(api.getListId(listName),['content','completed'])
    todosBare = [x[0] for x in todos]
    return render_template('todos.html',todos=todosBare,listName=listName)
