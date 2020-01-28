import numpy as np
import matplotlib.pyplot as plt
import sqlite3

roadName = "G107"
plotArrayX = []
plotArrayY = []

plt.title("Vehicle Track")

con = sqlite3.connect("/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/statistic.db")
cursors = con.execute("SELECT * FROM {};".format(roadName))
for cursor in cursors:
    (x, y) = cursor
    plotArrayX.append(x)
    plotArrayY.append(1-y)

plt.scatter(plotArrayX, plotArrayY)

plt.show()
