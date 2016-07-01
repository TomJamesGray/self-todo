# self-todo
## A simple self hosted todo list

The main point of this repo is to provide the api however it also contains 
a client which can be invoked by running src/main.py however this client is somewhat
limited but is still functional

### Dependencies:
* mysql
* pytest
* oursql3

### How to use it
Firstly you will need to set up a databse with the correct schema (found in dump.sql)
This schema can created in the database by running 

```
$ mysql -e "CREATE DATABSE IF NOT EXISTS self_todo" -u username -p
$ mysql -u username -p self_todo < dump.sql
```

You can change the name of the database if you want to however you will also have
to update the dbName in the db section of the config file

If you would like to run the client then run the command `python src/main.py`, help
is available via the help command
