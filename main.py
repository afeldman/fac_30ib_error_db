#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request, redirect, flash, render_template, url_for
from flask import g, jsonify, render_template, request, abort, make_response, session
import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from threading import Thread
import json
import os

db_host = ''
flask_host = ''

try:
	db_host = os.environ["DB_HOST"] 
        flask_host = os.environ["FLASK_HOST"]
except:
	db_host = 'localhost'
        flask_host = 'localhost'

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
app.config.update(dict(DEBUG=True,
                       RDB_HOST=db_host,
                       RDB_PORT=28015,
                       DB_NAME='fanuc',
                       TABLE='ib30_error'))

# ---------------- DB Setting ------------------

@app.before_request
def before_request():
    try:
        g.rdb_conn = rdb.connect(host=app.config['RDB_HOST'],
                                 port=app.config['RDB_PORT'])
        g.rdb_conn.use(app.config['DB_NAME'])
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

def get_type(name):
    return rdb.table(app.config['TABLE']).filter({'type': name}).run(g.rdb_conn)

def get_title(name):
    return rdb.table(app.config['TABLE']).filter({'title': name}).run(g.rdb_conn)

def get_number(name):
    return rdb.table(app.config['TABLE']).filter({'number': name}).run(g.rdb_conn)

def get_error(name, number):
    return rdb.table(app.config['TABLE']).filter(
        (rdb.row('title').eq(name)) & (rdb.row('number').eq(number))
    ).run(g.rdb_conn)

def get_all():
    return list(rdb.table(app.config['TABLE']).run(g.rdb_conn))

def delete():
    for val in get_all():
        rdb.table(app.config['TABLE']).get(val['id']).delete().run(g.rdb_conn)

def insert(title, typ, number, cause, desc, remedy):
    rdb.table(app.config['TABLE']).insert({"title": title,
                                           "type": typ,
                                           "number": number,
                                           "cause": cause,
                                           "desc": desc,
                                           "remedy": remedy}).run(g.rdb_conn)


#--------------------- URL --------------
@app.route('/')
def index():
    data = jsonify(get_all())
    return data

@app.route('/type/<string:typ>')
def type_t(typ):
    data = list(get_type(typ.upper()))
    return jsonify(data)

@app.route('/no/<string:number>')
def no(number):
    data = list(get_number(number))
    return jsonify(data)

@app.route('/title/<string:name>')
def name(name):
    data = list(get_title(name.upper()))
    return jsonify(data)

@app.route('/error/<string:name>/<string:number>')
def error_t(name,number):
    data = list(get_error(name.upper(),number))
    return jsonify(data)

@app.route('/delete/<string:id>')
def delete(id):
    data = delete(id)
    return jsonify(data)

#test curl -H "Content-Type: application/json" -X POST -d '{"title":"test","type":"WARN","number":"001","cause":"","desc":"","remedy":""}'  http://127.0.0.1:5000/
@app.route('/', methods=['POST'])
def add():
    if (request.is_json) :
        content = request.get_json()
        data = insert(title=content['title'],
                      typ=content['type'],
                      number=content['number'],
                      cause=content['cause'],
                      desc=content['desc'],
                      remedy=content['remedy'])
        return jsonify(data)
    else:
        return 'ERROR Message'
                   
#-------------------- main --------------
if __name__ == '__main__':
    app.run(debug = True, host=flask_host)
