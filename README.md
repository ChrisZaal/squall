pysquall
====

Database Adapter for multiple sql vendors, one command fits all.

Some functionality of the RDBMS may be squelched for massive
compatibility of all relational databases.

A list of databases I want to utilize in this adapter software are:

* sqlite3 - successfully written, basic tests implemented
* sqlserver - current driver project
* mysql
* postgres
* firebird


This software should have contributers from all database systems
that want to contribute.

Functionality that must be sustained:

* SELECT
* INSERT
* UPDATE
* DELETE
* (if applicable) Change Database on the Fly -- sqlite3 requires the path.
* Safe Transactions (rollback on error)

This software aims to be a solid single-threaded application first and 
foremost. Multi-threading can be implemented at a later date.

How to use this software
----

Sql Server
---------
```
import squall

self.sqlobj = squall.Session().connect('rfid', adapter='sqlserver', trusted=True, driver='SQL Server')
self.module = squall.db('sqlserver')
self.sqlobj.[command](sql, param)
```

( PLEASE NOTE THAT USING USERNAME AND PASSWORD NOT TESTED, BUT MAY FUNCTION... )

OR

Sqlite3 
---------
```
import squall
self.sqlobj = squall.Session().connect('rfid.db', adapter='sqlite3')
self.module = squall.db('sqlite3')

self.sqlobj.[command](sql, param)
```
 
