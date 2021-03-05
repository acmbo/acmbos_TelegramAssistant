# -*- coding: utf-8 -*-

import sqlite3




def connect(dbpath: str):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    return conn, c

    

def exec_wrapper(dbpath: str, statement: str, var=''):
    '''
    Executionwrapper. Function to speed up connection and excecution process

    Parameters
    ----------
    dbpath : str
        Database path
    statement : str
        SQLite statment
    var : str or list of str, optional
        If you use staments with values to replace (which are symbolized by a ?)
        you can add the string or a list of strings to the var variable, and 
        replace it automaticly
        The default is ''.

    Raises
    ------
    Exception
        Couldnt excecute command

    Returns
    -------
    None.

    '''
    conn = sqlite3.connect(dbpath)
    try:
        
        c = conn.cursor()
        print(statement)
        c.execute(statement, var)
        conn.commit()
        conn.close()
    
    except:
        conn.close()
        raise Exception('db command failed.')




def fetchallrows(dbpath:str, statement:str):
    """
    Fetches the return of a exceution on the sqlitedatabase

    Parameters
    ----------
    dbpath : str
        Databsepath
    statement : str
        Excecutionstatement

    Raises
    ------
    Exception
        Error in excecutionstatement ord db path

    Returns
    -------
    rows : TYPE
        list of entries in the database

    """
    conn, c = connect(dbpath)
    rows = []
    try:
        print(statement)
        c.execute(statement)
        rows = c.fetchall()   #complette row
        conn.commit()
        conn.close()
    except:
        conn.close()
        raise Exception("Error while executing")
    return rows




def activateForeignkeys(dbpath: str):
    statement = '''PRAGMA foreign_keys = ON;''' 
    exec_wrapper(dbpath, statement, var='')
  


def removeTable(table: str,dbpath: str):
    statement = '''DROP TABLE {table}'''.format(table=table) 
    exec_wrapper(dbpath, statement)



def removeView(view: str,dbpath: str):
    statement = '''DROP VIEW {view}'''.format(view=view) 
    exec_wrapper(dbpath, statement)



def rowcount(dbpath, entity):
    statement = 'SELECT COUNT(*) FROM {entity}'.format(entity=str(entity))
    return fetchallrows(dbpath, statement)[0][0]


def getallrows(dbpath, table):
    statement = f"SELECT * FROM {table}"
    return fetchallrows(dbpath, statement)


def deleterowbyid(dbpath, table, _id):
    statement = f"DELETE FROM {table} WHERE ID={_id}"
    return fetchallrows(dbpath, statement)

def deleterowbynamecol(dbpath, table, name):
    statement = f"DELETE FROM {table} WHERE name={name}"
    return fetchallrows(dbpath, statement)