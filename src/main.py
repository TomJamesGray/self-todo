#!/usr/bin/env python3
from flask import Flask,render_template,request,redirect,url_for
from src.api import Api

app = Flask(__name__)
api = Api('192.168.1.2','example','password','self_todo')

@app.route('/')
def index():
    #Get lists and get the list names out of the tuple
    lists = api.getLists()
    listsBare = [x[0] for x in lists]
    return render_template('index.html',lists=listsBare)

@app.route('/list/<listName>')
def showTodos(listName):
    todos = api.getListItems(api.getListId(listName),['content','completed'])
    todosBare = [x[0] for x in todos]
    return render_template('todos.html',todos=todosBare,listName=listName)

@app.route('/list/create')
def createList():
    listName = request.args.get('listName')
    print(listName)
    api.createList(listName)
    return redirect(url_for('index'))
