import sys
sys.path.insert(0, '/Share/PythonLib')

import Vehicle_Generator
import Vehicle_Tree

class Generator(Vehicle_Generator.Vehicle_Generator):
    def __init__(self):
        super().__init__(Vehicle_Tree.TreeDB("/Share/Main_Data", "tree.db"))
    
    def getRoadIndex(self, roadNameKey:str) -> list:
        roadIndex = []
        self.treedb.db.execute("PRAGMA case_sensitive_like=ON;")
        cursors = self.treedb.db.execute("SELECT name FROM sqlite_master WHERE type='table' and name LIKE '%{}%';".format(roadNameKey))
        self.treedb.db.execute("PRAGMA case_sensitive_like=OFF;")
        for cursor in cursors:
            roadIndex.append(cursor[0])
        return roadIndex
    
    def getRoadTimeline(self, roadName:str) -> list:
        timeline = []
        cursors = self.treedb.db.execute("SELECT DATE FROM {}".format(roadName))
        for cursor in cursors:
            timeline.append(cursor[0])
        
        return timeline