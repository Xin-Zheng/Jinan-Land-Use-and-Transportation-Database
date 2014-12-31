'''
Created on 20141018

@author: xiaogelunbu
'''

import arcpy
import os

arcpy.env.overwriteOutput=True


fcparcel=arcpy.GetParameterAsText(0)
fcpubroad=arcpy.GetParameterAsText(1)
greenfield=arcpy.GetParameterAsText(2)
addfieldname=arcpy.GetParameterAsText(3)

arcpy.DeleteField_management(fcpubroad,"greenlen")
arcpy.AddField_management(fcpubroad,"greenlen","FLOAT")
arcpy.DeleteField_management(fcpubroad,"length")
arcpy.AddField_management(fcpubroad,"length","FLOAT")

fieldexpression="!shape.length!/100*!"+greenfield+"!"
arcpy.CalculateField_management (fcpubroad, "greenlen" , fieldexpression ,"PYTHON_9.3")
fieldexpression="!shape.length!"
arcpy.CalculateField_management (fcpubroad, "length" , fieldexpression ,"PYTHON_9.3")

def spatialjoinsum(intar,injoin,infieldname,outfieldname,jointype):
    tempData = arcpy.env.scratchGDB + os.path.sep+"output"
    targetFeatures = intar
    joinFeatures = injoin
  
    # Create a new fieldmappings and add the two input feature classes.
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(targetFeatures)
    fieldmappings.addTable(joinFeatures)
 
    FieldIndex = fieldmappings.findFieldMapIndex(infieldname)
    fieldmap = fieldmappings.getFieldMap(FieldIndex)
 
    # Get the output field's properties as a field object
    field = fieldmap.outputField
 
    # Rename the field and pass the updated field object back into the field map
    field.name = outfieldname
    fieldmap.outputField = field
 
    # Set the merge rule to mean and then replace the old fieldmap in the mappings object
    # with the updated one
    fieldmap.mergeRule = "sum"
    fieldmappings.replaceFieldMap(FieldIndex, fieldmap)
 
    # Remove all output fields from the field mappings, except fields "Street_Class", "Street_Name", & "Distance"
    for field in fieldmappings.fields:
        if field.name not in ["FID",outfieldname]:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))
 
    #Run the Spatial Join tool, using the defaults for the join operation and join type
    arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, tempData, "#", "#", fieldmappings,jointype)
    arcpy.DeleteField_management(intar, outfieldname)
    arcpy.JoinField_management(intar, "FID", tempData, "TARGET_FID", [outfieldname])
    arcpy.Delete_management(tempData)

spatialjoinsum(fcparcel,fcpubroad,"greenlen","sumgreen","CONTAINS")
spatialjoinsum(fcparcel,fcpubroad,"length","sumlength","CONTAINS")

arcpy.DeleteField_management(fcparcel,addfieldname)
arcpy.AddField_management(fcparcel,addfieldname,"FLOAT")

cur = arcpy.UpdateCursor(fcparcel)
for row in cur: 
    newsumlength=row.getValue("sumlength")
    if newsumlength!=0:
        row.setValue(addfieldname, row.sumgreen/newsumlength)
        cur.updateRow(row)
    else:
        row.setValue(addfieldname, 0)
        cur.updateRow(row)

arcpy.DeleteField_management(fcparcel,["sumgreen","sumlength"])



