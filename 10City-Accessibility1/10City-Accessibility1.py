'''
Created on 20141023

@author: xiaogelunbu
'''

import arcpy
import os

arcpy.env.overwriteOutput=True


fcparcel=arcpy.GetParameterAsText(0)
poilayer=arcpy.GetParameterAsText(1)
addfieldname=arcpy.GetParameterAsText(2)

tempData = arcpy.env.scratchGDB + os.path.sep+"parcelpoint"
temptable = arcpy.env.scratchGDB + os.path.sep+"outtable"
temptable2 = arcpy.env.scratchGDB + os.path.sep+"outtable2"

arcpy.FeatureToPoint_management(fcparcel, tempData)
arcpy.PointDistance_analysis(tempData, poilayer, temptable)
arcpy.DeleteField_management(fcparcel,"SUM_ca")


arcpy.DeleteField_management(temptable,"ca")
arcpy.AddField_management(temptable,"ca","FLOAT")

cur = arcpy.UpdateCursor(temptable)
for row in cur: 
    newdistance=row.getValue("DISTANCE")
    if newdistance!=0:
        row.setValue("ca", 1.0/newdistance**2)
        cur.updateRow(row)
    else:
        row.setValue("ca", 0)
        cur.updateRow(row)


arcpy.Statistics_analysis(temptable, temptable2, [["ca","SUM"]], "INPUT_FID")
arcpy.JoinField_management(fcparcel, "FID", temptable2, "INPUT_FID", ["SUM_ca"])


arcpy.DeleteField_management(fcparcel,addfieldname)
arcpy.AddField_management(fcparcel,addfieldname,"FLOAT")
arcpy.CalculateField_management (fcparcel, addfieldname , "!SUM_ca!" ,"PYTHON_9.3")
arcpy.DeleteField_management(fcparcel,"SUM_ca")

arcpy.Delete_management(tempData)
arcpy.Delete_management(temptable)
arcpy.Delete_management(temptable2)


