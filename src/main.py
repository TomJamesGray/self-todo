#!/usr/bin/env python3
from configparser import SafeConfigParser
from flask import Flask
import os
import oursql
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "Show all todo lists"

@app.route('/list/<listName>')
def show_todos(listName):
    return "Show todos for specified list " + listName


