#!/usr/bin/env python
import rethinkdb as rdb
import json
from tqdm import tqdm
import os

db_host = ''

try:
	db_host = os.environ["DB_HOST"] 
except:
	db_host = 'localhost'

r = rdb.RethinkDB()

r.connect( db_host, 28015 ).repl()
try:
	r.db_create("fanuc").run()
except rdb.errors.ReqlOpFailedError:
	print("database exists")

try:
	r.db("fanuc").table_create("ib30_error").run()
except rdb.errors.ReqlOpFailedError:
	print("table exists")

data = json.load(open('./asset/fanuc_error.json'))

for elem in tqdm(data):
    r.db("fanuc").table("ib30_error").insert(elem).run()

r.db("fanuc").table("ib30_error").index_create('number').run()
r.db("fanuc").table("ib30_error").index_wait("number").run()
r.db("fanuc").table("ib30_error").index_create('title').run()
r.db("fanuc").table("ib30_error").index_wait("title").run()
