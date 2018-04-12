#!/usr/bin/env python
import rethinkdb as r
import json
import os

data = json.load(open('./asset/fanuc_error.json'))

db_host = ''

try:
	db_host = os.environ["DB_HOST"] 
except:
	db_host = 'localhost'

print db_host

r.connect( db_host, 28015 ).repl()
r.db_create("fanuc").run()
r.db("fanuc").table_create("ib30_error").run()

for elem in data:
    r.db("fanuc").table("ib30_error").insert(elem).run()

r.db("fanuc").table("ib30_error").index_create('number').run()
r.db("fanuc").table("ib30_error").index_wait("number").run()
r.db("fanuc").table("ib30_error").index_create('title').run()
r.db("fanuc").table("ib30_error").index_wait("title").run()
