import Vehicle_Data
import Vehicle_Tree

class Vehicle_Generator:
    def __init__(self, treedb):
        '''
        Vehicle_Generator(Vehicle_Tree.TreeDB)
        '''
        self.treeDict = {}
        self.treedb = treedb
    
    def getIndexDB(self, roadName, date):
        try:
            filePath = self.treedb.findData(roadName, date)
        except:
            return None
        if (filePath == "0"):
            # Have not this data
            return None
        return Vehicle_Data.IndexDB(filePath)
    
    def initData(self, roadName, date):
        '''
        Vehicle_Generator.initData(str, str) -> Successful? True:False

        date:"YYYY-MM-DD"
        '''
        indexDB = self.getIndexDB(roadName, date)
        if (indexDB == None):
            return False

        if (not roadName in self.treeDict):
            self.treeDict[roadName] = {}
        if (not date in self.treeDict[roadName]):
            self.treeDict[roadName][date] = indexDB
        return True