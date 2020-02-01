import time
import hashlib
import sqlite3
import os

def str2sha256(s):
    '''
    str2sha256(str) -> str
    '''
    sha = hashlib.sha256()
    sha.update(s.encode('utf-8'))
    return sha.hexdigest()

def getDate():
    '''
    getDate(void) -> "YYYY-MM-DD"
    '''
    string_time = time.strftime("%Y-%m-%d", time.localtime())
    return string_time

def getTime():
    '''
    getTime(void) -> "HH:MM:SS"
    '''
    string_time = time.strftime("%H:%M:%S", time.localtime())
    return string_time

class TreeDB:
    def __init__(self, treePath, db_name):
        self.treePath = treePath
        self.db_name = db_name
        self.db = sqlite3.connect("{}/{}".format(treePath, db_name), check_same_thread=False)
    
    def findData(self, roadName, date):
        '''
        TreeDB.findData(str, str) -> str

        Return paired db filePath. If fair, return "0"
        '''

        try:
            cursors = self.db.execute("SELECT FILENAME FROM {} WHERE DATE IS \"{}\";".format(roadName, date)).fetchone()
            try:
                filename = cursors[0]
                return "{}/{}/index.db".format(self.treePath, filename)
            except:
                return "0"
        except sqlite3.OperationalError:
            return "0"
    
    def insertData(self, roadName, date):
        hash_data = str2sha256("{}{}".format(roadName, date))
        if (not self.hasRoad(roadName)):
            self.createTable(roadName)
        self.db.execute("INSERT INTO {} VALUES (\"{}\", \"{}\");".format(roadName, date, hash_data))
        os.makedirs("{}/{}".format(self.treePath, hash_data))
        self.db.commit()

    def createTable(self, roadName):
        '''
        TreeDB.createTable(str)
        '''
        self.db.execute("CREATE TABLE {}(DATE TEXT NOT NULL, FILENAME TEXT NOT NULL);".format(roadName))
        self.db.commit()
    
    def hasRoad(self, roadName):
        '''
        Judge if the table exist
        '''
        try:
            self.db.execute("SELECT * FROM {};".format(roadName))
            return True
        except:
            return False