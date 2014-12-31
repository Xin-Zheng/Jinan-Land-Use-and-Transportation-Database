'''
Created on 20141023

@author: xiaogelunbu
'''

import arcpy
import os
import math

arcpy.env.overwriteOutput=True


fcparcel=arcpy.GetParameterAsText(0)
poilayer=arcpy.GetParameterAsText(1)
betavalue=arcpy.GetParameterAsText(2)
addfieldname=arcpy.GetParameterAsText(3)



tempDatapar = arcpy.env.scratchGDB + os.path.sep+"parpoi"
temptable = arcpy.env.scratchGDB + os.path.sep+"out"
temptable2 = arcpy.env.scratchGDB + os.path.sep+"outt"
tempDatajoin=arcpy.env.scratchGDB + os.path.sep+"join"

arcpy.FeatureToPoint_management(fcparcel, tempDatapar)
arcpy.PointDistance_analysis(tempDatapar, tempDatapar, temptable)

arcpy.SpatialJoin_analysis(fcparcel, poilayer, tempDatajoin,"#","#","CONTAINS")
arcpy.DeleteField_management(temptable, "Join_Count")
arcpy.JoinField_management(temptable, "NEAR_FID", tempDatajoin, "TARGET_FID", ["Join_Count"])
arcpy.Delete_management(tempDatajoin)


arcpy.DeleteField_management(temptable,"cal")
arcpy.AddField_management(temptable,"cal","FLOAT")

betanum=float(betavalue)
cur = arcpy.UpdateCursor(temptable)
for row in cur: 
    row.setValue("cal", row.Join_Count*math.exp((-1.0)*betanum*row.DISTANCE))
    cur.updateRow(row)

arcpy.Statistics_analysis (temptable, temptable2, [["cal","SUM"]], ["INPUT_FID"])

arcpy.JoinField_management(fcparcel, "FID", temptable2, "OID", ["SUM_outt"])
arcpy.Delete_management(temptable2)

arcpy.DeleteField_management(fcparcel, addfieldname)
arcpy.CalculateField_management (fcparcel, addfieldname , "!SUM_outt!" ,"PYTHON_9.3")

