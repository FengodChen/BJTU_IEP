import Vehicle_Tree
import Vehicle_Data
a = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
path = a.findData("NanJingRoad", Vehicle_Tree.getDate())
t = Vehicle_Data.IndexDB(path)
t.initRoadLine()
t.insertData([1,2,3],[4,5,6],[7,8,9])
t.insertData([1324,2234,356],[4234,534,634],[756,8342,934])

import Vehicle_Tree
import Vehicle_Data
import Vehicle_Generator
treedb = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
gen = Vehicle_Generator.Vehicle_Generator(treedb)
gen.initData("NanJingRoad", "2020-01-20")
gen.initData("NanJingRoad", "2020-01-21")