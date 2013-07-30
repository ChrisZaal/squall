#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Daniel Kettle
# Date:   July 25 2013
#

'''
TODO: How to init an adapter, how to call it/close it

FIXME: Threading 
'''

ADAPTERS = {'sqlite3' : None,
            'sqlserver': None, # Uses odbc drivers
            'mysql': None,
            'postgres': None,
            'firebird': None}

class Session(object):
    '''
    :Description:
        Generic adapter class for the Database
        
        Use this class to import adapters. A list of adapters can be
        generated by this class if you need to parse through them;
        
        By using this class, one feature of squall is to connect to 
        multiple databases simultaneously via a singleton thread per
        database
    '''
    
    def __init__(self, db_type, db_name, db_host="localhost"):
        '''
        :Description:
            Contains a pool of connections that are identified by the
            db_type, db_name and db_host parameters. If all 3 values 
            are the same as another existing connection, it will fail.
            
        :Parameters:
            - db_type: string; Name of Adapter
                - Ex: "mysql" or "sqlite3"
            - db_name: string; Name of the Database to connect to
            - db_host: string; Address of the Database
                - Default is "localhost"
                
        :Throws:
            - UndefinedAdapterException: Requesting connection to an unknown
              database. Squall will not be able to find an adapter.
            - DatabaseNotFound: Selecting a Database that does not exist.
            - (a timeout exception for remote databases?)
            - (remote database could not connect, for invalid permissions or 
               login info, etc)
            - AdapterException: Problem with adapter, encompassess all possible
              adapter errors
        '''
        # Collection of database connections

        if not db_type in ADAPTERS.keys():
            raise AdapterException('No Database Type Found' + db_type)
        
        self.pool = {db_host: {db_type: {db_name: None}}}
        self.broadcast = True   # Sends all db commands to all conns in pool
        
        
    def connect(self, db_type, db_name, db_host='localhost'):
        '''
        :Description:
            Attempts to connect to a database; if an identical connection exists
            that you connect to, the software raises an 
            AlreadyConnectedException.
            
            If a connection is successfully made, it will add itself to the db
            pool. 
        '''
        # Fetch adapter
        # Connect using adapter
        # Add adapter to pool
        # Return object on success or None
        
        if not db_type in ADAPTERS.keys():
            raise(AdapterException("Unknown Database Type"))
        self.pool[db_host][db_type][db_name] = ADAPTERS[db_type].connect(db_name, db_host)
    
    def disconnect(self, db_type, db_name, db_host='localhost'):
        '''
        :Description:
            Safely remove a python db adapter from the pool.
        '''
        
        self.pool[db_host][db_type][db_name].disconnect()
        self.pool[db_host][db_type][db_name] = None
    
        
    def insert(self, db_type, db_name, db_host, sql, *args):
        '''
        :Descriptions:
            Insert into the database. Actual sql will be determined at a later
            date. The Sqlite3 format from python-sqlite is simple and 
            effective.
            
        :Parameters:
            - sql: string; an sql statement. '?' characters imply a required 
              argument in the statement. 
              
        :Throws:
            - ArgumentMismatchException: When the number of '?' doesn't match
              up with the length of arguments supplied to the method.
            - RollbackException: An error occured in sending the sql statement
              to the database.  
        '''
        return self.pool[db_host][db_type][db_name].insert(sql, tuple(args))
        
    def update(self, db_type, db_name, db_host, sql, *args):
        return self.pool[db_host][db_type][db_name].update(sql, tuple(args))
    
    def delete(self, db_type, db_name, db_host, sql, *args):
        return self.pool[db_host][db_type][db_name].delete(sql, tuple(args))
    
    def select(self, db_type, db_name, db_host, sql, *args):
        return self.pool[db_host][db_type][db_name].select(sql, tuple(args))
    
def db(db_type):
    '''
    :Description:
        Method assigns the imported SqlAdapter, or api object, into the
        ADAPTERS dictionary. 
        
        Please note that this method returns the module, so if you need
        methods that stem directly from the import itself (such as
        exceptions), you will need to place the return value into
        its own variable or re-call this method with the same parameters.
    '''
    import sys,importlib 
    sys.path.append('adapters')
    module = None
    if db_type == 'sqlite3':
        module = importlib.import_module('sqlite3')
        if not module is None:
            api = importlib.import_module('squallsqlite3').SqlAdapter(module)
            ADAPTERS[db_type] = api
    return module
    
class AdapterException(Exception):
    
    def __init__(self, message):
        Exception.__init__(self, message)