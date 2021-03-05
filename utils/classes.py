# -*- coding: utf-8 -*-

import sqlite3

class DatabaseManager(object):
    def __init__(self, db):
        """
        Class for managing Connection to Database

        Parameters
        ----------
        db : str
            database path

        Returns
        -------
        None.

        """
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()