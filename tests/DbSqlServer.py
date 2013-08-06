#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Daniel Kettle
# Date:   July 29 2013
#

import sys, os
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..', 'adapters'))

import unittest
import squall
from squallsql import Table, Fields, Value, Transaction, Where
import squallserver as tsql

class Test(unittest.TestCase):


    def setUp(self):
        self.sqlobj = squall.Session().connect('rfid', adapter='sqlserver', trusted=True, driver='SQL Server')
        self.module = squall.db('sqlserver')
        
        self.sqlselect = tsql.Select(Table('t'), Fields('*'), Where('x', '=', Value(1)))
        
    
        assert not self.module is None, 'Python Driver not imported successfully'
        assert not self.sqlobj is None, 'Squallserver not imported correctly or invalid'
        self.sqlobj.sql('CREATE TABLE t(x INTEGER, y INTEGER, z INTEGER, CONSTRAINT x_pk PRIMARY KEY(x))', ())
        self.sqlobj.commit()
    
    def testSelect(self):
        print("Test: Select Insert Statement")
        assert self.sqlobj.select('SELECT * FROM t WHERE x = ?', (1,)), 'Select Statement Errored'

    def testInsertAndDelete(self):
        print("Test: Inserting test data into t table")
        self.sqlobj.insert('INSERT INTO t (x, y, z) VALUES (?, ?, ?)', (1, 2, 3))
        self.sqlobj.commit()
        print("Test: Selecting data we inserted")
        self.sqlobj.select('SELECT x, y, z FROM t WHERE x = 1', ())
        # Should error if fails
        self.sqlobj.delete('DELETE FROM t WHERE x = 1', ())
        self.sqlobj.commit()

    def testUpdate(self):
        print("Test: Inserting a record")
        self.sqlobj.insert('INSERT INTO t (x, y, z) VALUES (?, ?, ?)', (5, 4, 3))
        print("Test: Updateding a record")
        self.sqlobj.update('UPDATE t SET y = ? WHERE x = ?', (9999, 5))
        print("Test: Selecting Record")
        self.sqlobj.commit()
        print("Test: Select Statement")
        self.sqlobj.select('SELECT x, y, z FROM t WHERE y = 9999', ())
        self.sqlobj.delete('DELETE FROM t WHERE x = 5', ())
        self.sqlobj.commit()
        
        
    def tearDown(self):
        print("Closing connection to SQL Server on local machine")
        self.sqlobj.sql('DROP TABLE t;', ())
        self.sqlobj.commit()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()