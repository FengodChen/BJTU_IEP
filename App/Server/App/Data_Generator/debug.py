import Vehicle_Tree
import Vehicle_Data
a = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
path = a.findData("NanJingRoad", Vehicle_Tree.getDate())
t = Vehicle_Data.IndexDB(path)
t.initRoadLine()
t.insertData([1,2,3],[4,5,6],[7,8,9])
t.insertData([1324,2234,356],[4234,534,634],[756,8342,934])

# Vehicle Generator

import Vehicle_Tree
import Vehicle_Data
import Vehicle_Generator
treedb = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
gen = Vehicle_Generator.Vehicle_Generator(treedb)
gen.initData("NanJingRoad", "2020-01-20")
idb = gen.treeDict["NanJingRoad"]["2020-01-20"]
d = idb.getData("18:00:16")

# Get Date Range
import datetime

start='2019-01-01'
end='2019-01-07'
datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
 
data_list = list()
while datestart<=dateend:
    data_list.append(datestart.strftime('%Y-%m-%d')) 
    datestart+=datetime.timedelta(days=1)

print(data_list)

# Get Time Range
import datetime

start='18:01:01'
end='19:01:07'
datestart=datetime.datetime.strptime(start,'%H:%M:%S')
dateend=datetime.datetime.strptime(end,'%H:%M:%S')
 
data_list = list()
while datestart<=dateend:
    data_list.append(datestart.strftime('%H:%M:%S')) 
    datestart+=datetime.timedelta(seconds=1)

print(data_list)