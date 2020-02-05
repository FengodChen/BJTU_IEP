import sys
sys.path.insert(0, '/Share/PythonLib')

import Vehicle_Generator
import Vehicle_Tree

class Generator(Vehicle_Generator.Vehicle_Generator):
    def __init__(self):
        super().__init__(Vehicle_Tree.TreeDB("/Share/Main_Data", "tree.db"))
    
    def getRoadIndex(self, roadNameKey) -> list:
        '''
        keys: type=str
        '''
        roadIndex = []
        cursors = self.treedb.db.execute("SELECT name FROM sqlite_master WHERE type='table' and name LIKE '{}%';".format(roadNameKey))
        for cursor in cursors:
            roadIndex.append(cursor[0])
        return roadIndex
    