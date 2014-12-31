'''
Created on 2014.11.12

@author: xiaogelunbu
'''


import arcpy
import os

arcpy.env.overwriteOutput=True


fcparcel=arcpy.GetParameterAsText(0)
fcpoi=arcpy.GetParameterAsText(1)



#CROSS POI SUM
tempData = arcpy.env.scratchGDB + os.path.sep+"output"
arcpy.SpatialJoin_analysis(fcparcel, fcpoi, tempData,"#","#","CONTAINS")

arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["Join_Count"])
arcpy.Delete_management(tempData)

arcpy.DeleteField_management(fcparcel, "poi过街点")
arcpy.AddField_management(fcparcel,"poi过街点","FLOAT")
fieldexpression="!Join_Count!"
arcpy.CalculateField_management (fcparcel, "poi过街点" , fieldexpression ,"PYTHON_9.3")
arcpy.DeleteField_management(fcparcel,"Join_Count")





#CROSS DENSITY
arcpy.DeleteField_management(fcparcel,"poi过街密")
arcpy.AddField_management(fcparcel,"poi过街密","FLOAT")

cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    length=row.getValue("n市政路长")
    num=row.getValue("poi过街点")
    if length!=0:
        row.setValue("poi过街密", num/length)
        cur.updateRow(row)
    else:
        row.setValue("poi过街密", 0)
        cur.updateRow(row)


