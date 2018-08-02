# fac_30ib_error_db
FANUC provides an alarm error message code book to look for the errors raised when working with the robot. This project builds a database utilizing [RethinkDB](https://www.rethinkdb.com) with the information for the errors.

## Setup the server
To start the application build the database. Therefor first setup the database, start the database and run the bootstrap.py script

```bash
export DB_HOST=<database communication address>
./bootstrap.py
```

## Start the RESTfull server
To start the server setup the environmental information.  

```bash
export DB_HOST=<database communication address>
export FLASK_HOST=<flask communication address>
```

Then you are able to start the server.

```bash
./main.py
```

## Accessing the Server
The server response all information using utilizing JSON.
