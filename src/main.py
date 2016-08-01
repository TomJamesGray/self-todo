#!/usr/bin/env python3
import flask_login
from functools import wraps
from flask import g,Flask,render_template,request,redirect,url_for
from src.api import Api
from src.helpers import getConfPart
from src.user import User

app = Flask(__name__)
app.secret_key = "SECRET"
loginManager = flask_login.LoginManager()
loginManager.init_app(app)
#Get config parts for the api
host = getConfPart("db","host")
user = getConfPart("db","user")
password = getConfPart("db","password")
dbName = getConfPart("db","dbName")
#Make instance of api using db paramaters from
#config file
api = Api(host,user,password,dbName)

@app.route('/')
@app.route('/lists')
@flask_login.login_required
def index():
    lists = api.getLists(flask_login.current_user.get_id(),['listName','listId'])
    return render_template('index.html',lists=lists)

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
    if listName == "":
        return redirect(url_for('index'))
    api.createList(listName,flask_login.current_user.get_id())
    return redirect(url_for('index'))

@app.route('/list/delete')
def deleteList():
    for listId in request.args.getlist('list'):
        print(listId)
        api.removeList(listId)

    return redirect(url_for('index'))

@app.route('/list/<listName>/create')
def createTodo(listName):
    listId = api.getListId(listName)
    content = request.args.get('content')
    completed = int(request.args.get('completed',0))
    api.saveListItem(listId,content,completed)
    return redirect(url_for('showTodos',listName=listName))

"""
User login and other user functionality
"""
@loginManager.user_loader
def userLoader(userId):
    if api.isUser(userId):
        return User(userId)
    else:
        return None

@loginManager.request_loader
def requestloader(request):
    userId = request.form.get('userId')
    if api.isUser(userId):
        return User(userId)
    else:
        return None

@loginManager.unauthorized_handler
def unoauthorized():
    return "Unortharized"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userName = request.values.get('userName')
        password = request.values.get('password')
        print("user:{}".format(userName))
        #Validate user against password
        if api.validateUser(userName,password):
            #User is valid
            userId = api.getUserId(userName)
            flask_login.login_user(User(userId),remember=True)
            return redirect(url_for('secret'))
        else:
            #User isn't valid, return to login page
            return render_template('login.html')
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return "Logged out"

#Testing purposes only
@app.route('/secret')
@flask_login.login_required
def secret():
    return "Logged in as: {}".format(flask_login.current_user.get_id())

