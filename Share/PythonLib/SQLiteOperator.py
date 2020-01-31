import Numpy_String
import sqlite3

class BaseOperator:
    def __init__(self, db_path, rw, check_same_thread = True):
        self.db = sqlite3.connect(db_path, check_same_thread = check_same_thread)
        self.__rw = rw
    
    def args2str(self, args):
        arg_str = ""
        for arg in args:
            arg_str = "{}, {}".format(arg_str, arg)
        arg_str = arg_str[1:]
        return arg_str
    
    def createTable(self, table_name, args):
        '''
        args = [value1, value2, ..., valueN]
        '''
        col_str = self.args2str(args)
        self.db.execute("CREATE TABLE {} ({})".format(table_name, col_str))

    def read(self, table_name, col = "*", condition = None) -> list:
        '''
        col = "column1, column2, ..., columnN" or "*"

        condition is what after "WHERE"
        '''
        list = []

        if (condition == None):
            cursors = self.db.execute("SELECT {} FROM {};".format(col, table_name))
        else:
            cursors = self.db.execute("SELECT {} FROM {} WHERE {};".format(col, table_name, condition))

        for cursor in cursors:
            list.append(cursor)
        
        return list

    def write(self, table_name, args, commit = True):
        '''
        args = [value1, value2, ..., valueN]
        '''
        if (self.__rw):
            args_str = self.args2str(args)
            self.db.execute("INSERT INTO {} VALUES ({});".format(table_name, args_str))
            if (commit):
                self.db.commit()
        else:
            raise Exception("Cannot write because this BaseOperator define db file read-only file")