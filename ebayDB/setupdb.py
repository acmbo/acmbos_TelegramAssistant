# -*- coding: utf-8 -*-

def main(dbpath):
    
    from ebayDB.sqlitedb import createTable, createPhotoTable,createViewofAllphotos
    
    createTable(dbpath) 
    createPhotoTable(dbpath)
    createViewofAllphotos(dbpath)
    createViewofAllItems(dbpath)

if __name__ == '__main__':
    
    dbpath = 'ebayDB/db/ebay.db'
    main(dbpath)
    