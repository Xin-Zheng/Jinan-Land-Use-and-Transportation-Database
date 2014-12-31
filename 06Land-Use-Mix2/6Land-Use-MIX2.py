

import arcpy
from arcpy import env
import math
import os



arcpy.env.overwriteOutput=True
tempData = arcpy.env.scratchGDB+os.path.sep+"output"

fcparcel=arcpy.GetParameterAsText(0)
fcpoi1=arcpy.GetParameterAsText(1)
fcpoi2=arcpy.GetParameterAsText(2)
fcpoi3=arcpy.GetParameterAsText(3)
fcpoi4=arcpy.GetParameterAsText(4)
addfieldname=arcpy.GetParameterAsText(5)


targetFeatures = fcparcel
joinFeatures1 = fcpoi1
joinFeatures2 = fcpoi2
joinFeatures3 = fcpoi3
joinFeatures4 = fcpoi4
a=0

#Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures1, tempData, "#", "#","CONTAINS")
arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["Join_Count"])
arcpy.AddField_management(fcparcel,"poi1count","FLOAT")
arcpy.CalculateField_management (fcparcel, "poi1count" , "!Join_Count!" ,"PYTHON_9.3")
cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    a=a+row.getValue("Join_Count")
arcpy.DeleteField_management(fcparcel, "Join_Count")
arcpy.Delete_management(tempData)


arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures2, tempData, "#", "#","CONTAINS")
arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["Join_Count"])
arcpy.AddField_management(fcparcel,"poi2count","FLOAT")
arcpy.CalculateField_management (fcparcel, "poi2count" , "!Join_Count!" ,"PYTHON_9.3")
cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    a=a+row.getValue("Join_Count")
arcpy.DeleteField_management(fcparcel, "Join_Count")
arcpy.Delete_management(tempData)


arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures3, tempData, "#", "#","CONTAINS")
arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["Join_Count"])
arcpy.AddField_management(fcparcel,"poi3count","FLOAT")
arcpy.CalculateField_management (fcparcel, "poi3count" , "!Join_Count!" ,"PYTHON_9.3")
cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    a=a+row.getValue("Join_Count")
arcpy.DeleteField_management(fcparcel, "Join_Count")
arcpy.Delete_management(tempData)


arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures4, tempData, "#", "#","CONTAINS")
arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["Join_Count"])
arcpy.AddField_management(fcparcel,"poi4count","FLOAT")
arcpy.CalculateField_management (fcparcel, "poi4count" , "!Join_Count!" ,"PYTHON_9.3")
cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    a=a+row.getValue("Join_Count")
arcpy.DeleteField_management(fcparcel, "Join_Count")
arcpy.Delete_management(tempData)


arcpy.DeleteField_management(fcparcel,addfieldname)
arcpy.AddField_management(fcparcel,addfieldname,"FLOAT")

cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    if a!=0:
        row.setValue(addfieldname, 1.0-(abs(row.poi1count/a-1.0/4.0)+abs(row.poi2count/a-1.0/4.0)+abs(row.poi3count/a-1.0/4.0)+abs(row.poi4count/a-1.0/4.0))*2.0/3.0)
        cur.updateRow(row)
    else:
        row.setValue(addfieldname, 0)
        cur.updateRow(row)



arcpy.DeleteField_management(fcparcel, ["poi1count","poi2count","poi3count""poi4count"])
arcpy.Delete_management(tempData)



