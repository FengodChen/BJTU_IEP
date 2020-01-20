import Vehicle_Data
import Vehicle_Tree
import json
import datetime

def getDateRange(startDate, endDate):
    dateList = []

    dateStart = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(endDate, '%Y-%m-%d')
     
    while (dateStart <= dateEnd):
        dateList.append(dateStart.strftime('%Y-%m-%d')) 
        dateStart += datetime.timedelta(days=1)
    
    return dateList

def getTimeRange(startTime, endTime):
    timeList = []

    timeStart = datetime.datetime.strptime(startTime, '%H:%M:%S')
    timeEnd = datetime.datetime.strptime(endTime, '%H:%M:%S')
     
    while (timeStart <= timeEnd):
        timeList.append(timeStart.strftime('%H:%M:%S')) 
        timeStart += datetime.timedelta(seconds=1)
    
    return timeList

class Vehicle_Generator:
    def __init__(self, treedb):
        '''
        Vehicle_Generator(Vehicle_Tree.TreeDB)
        '''
        self.treeDict = {}
        self.treedb = treedb
    
    def getIndexDB(self, roadName, date):
        '''
        Vehicle_Generator.getIndexDB(str, str) -> str

        Return indexDB path
        '''
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
    
    def data2json(self, data):
        return json.dumps(data)
    