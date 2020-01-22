import Vehicle_Tree
import Vehicle_Data
import Vehicle_Operator
treedb = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
opr = Vehicle_Operator.Vehicle_Operator(treedb)
sum_dict = opr.getData_DateRange("NanjingRoad", "2020-01-28", "2020-03-22", "12:00:00", "14:00:00")
opr.insertData("ABCRoad", "2022-01-01", "12:00:00", [[1,2,3], [4,5,6],[7,8,9]], ["Left", "Ahead", "Right"])
