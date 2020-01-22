import Vehicle_Tree
import Vehicle_Data
import Vehicle_Generator
treedb = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
gen = Vehicle_Generator.Vehicle_Generator(treedb)
sum_dict = gen.getData_DateRange("NanjingRoad", "2020-01-28", "2020-03-22", "12:00:00", "14:00:00")
gen.insertData("ABCRoad", "2022-01-01", "12:00:00", [[1,2,3], [4,5,6],[7,8,9]], ["Left", "Ahead", "Right"])
