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
    todos = api.getListItems(api.getListId(listName),['content','todoId','completed'])
    return render_template('todos.html',todos=todos,listName=listName)

@app.route('/list/<listName>/mark')
def markTodos(listName):
    #TODO Have ability to specify completion or incompletion
    #not just toggling
    todoIds = []
    for value in request.args.getlist('todo'):
        print(value)
        api.switchItemCompletion(value)
    
    return redirect(url_for('showTodos',listName=listName))

@app.route('/list/<listName>/delete')
def deleteTodos(listName):
    for value in request.args.getlist('todo'):
        print(value)
        api.removeListItem(value)

    return redirect(url_for('showTodos',listName=listName))

@app.route('/list/create')
def createList():
    listName = request.args.get('listName')
    print(listName)
    api.createList(listName)
    return redirect(url_for('index'))

@app.route('/list/<listName>/create')
def createTodo(listName):
    listId = api.getListId(listName)
    content = request.args.get('content')
    completed = int(request.args.get('completed',0))
    api.saveListItem(listId,content,completed)
    return redirect(url_for('showTodos',listName=listName))
