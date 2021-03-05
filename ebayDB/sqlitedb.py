# -*- coding: utf-8 -*-
"""
Übersicht der Commands mit Beispielen
-------------------------------------
-------------------------------------


Einfügen von einem Item, was die letzte Zeile zurückgibt
--------------------------------------------------------

from ebayDB.item import item
i = item(2,'test4')
i.setsize('1x2x3')  
 
lastrow_item = insertVAl(i, dbpath)



Einfügen von einem Photo
------------------------

insertPhoto(dbpath, lastrow_item, 'test', 'path')



Ausführen von Befehlen mit Return durch die DB
----------------------------------------------
tablename = 'ebayitem'
phototable = 'ebayphotos'


colnames = fetchallrows(dbpath,f"PRAGMA table_info({tablename})")
rows = fetchallrows(dbpath, f"SELECT * FROM {tablename}")
rows_photo = fetchallrows(dbpath, f"SELECT * FROM {phototable}")
rows2 = fetchallrows(dbpath, f"SELECT * FROM ebayitemphotos2")



Vorgefertigte Commands    
-----------------------
from ebayDB.sqlitecommands import removeTable, removeView, rowcount

count = rowcount(dbpath, 'ebayitem')    #returns rowcount
removeTable('ebayitem', dbpath)
removeTable('ebayphotos', dbpath)
removeView('ebayitemphotos2', dbpath)


"""



#import sqlite3
from ebayDB.sqlitecommands import exec_wrapper, connect, fetchallrows



def createTable(dbpath: str):
    statement = '''CREATE TABLE ebayitem (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL UNIQUE,
                                        length REAL,
                                        width REAL,
                                        height REAL,
                                        type TEXT,
                                        description TEXT,
                                        origin TEXT,
                                        startprice REAL,
                                        listingduration TEXT);'''  
    exec_wrapper(dbpath, statement, var='')
  




def createPhotoTable(dbpath: str):
    statement =  '''CREATE TABLE ebayphotos (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ebayitemid INTEGER NOT NULL,
                                        name TEXT,
                                        photopath TEXT NOT NULL,
                                        FOREIGN KEY (ebayitemid)
                                            REFERENCES ebayitem (id));'''
    exec_wrapper(dbpath, statement, var='')
   





def insertVAl(item, dbpath):
    queryval = [
        item.name,
        item.length.value,
        item.width.value,
        item.height.value,
        item.type ,
        item.description,
        item.origin,
        item.startprice,
        item.listingduration,]
    

    statement =  "INSERT INTO ebayitem (name,length, width, height,type,description,origin,startprice,listingduration) VALUES (?,?,?,?,?,?,?,?,?)"
    lastrowid = None
    conn, c = connect(dbpath)
    
    try:
        print(statement)
        c.execute(statement, queryval)
        lastrowid = c.lastrowid
        conn.commit()
        conn.close()
        return lastrowid
    
    except:
        conn.close()
        raise Exception("Error while executing")

    


def insertPhoto(dbpath: str, idx, name:str, path:str):
    
    conn, c = connect(dbpath)
    statement = "INSERT INTO ebayphotos (ebayitemid,name,photopath) VALUES (?,?,?)"
    lastrowid = None
    
    try:
        print(statement)
        c.execute(statement, [idx,name,path])
        lastrowid = c.lastrowid
        conn.commit()
        conn.close()
        return lastrowid
    
    except:
        conn.close()
        raise Exception("Error while executing")

    
    


def createViewofAllphotos(dbpath: str):
    statement = """CREATE VIEW ebayitemphotos AS
                                   SELECT 
                                       ebayitem.id AS ID,
                                       ebayitem.name AS Name,
                                       ebayphotos.photopath AS Photo
                                   FROM
                                       ebayphotos
                                       LEFT JOIN ebayitem
                                           ON ebayphotos.ebayitemid = ebayitem.id"""
    exec_wrapper(dbpath,statement)
    


def createViewofAllItems(dbpath: str):
    statement = """CREATE VIEW ebayitemsbotview AS
                                   SELECT 
                                       ebayitem.id AS ID,
                                       ebayitem.name AS Name,
                                       ebayitem.type AS Type
                                   FROM
                                       ebayitem"""
    exec_wrapper(dbpath,statement)


    
