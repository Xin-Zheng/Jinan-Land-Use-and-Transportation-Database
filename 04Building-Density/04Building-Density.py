'''
Created on 20141015


@author: xiaogelunbu
'''

import arcpy
from arcpy import env
import os



arcpy.env.overwriteOutput=True
tempData = arcpy.env.scratchGDB+os.path.sep+"output"


fcparcel=arcpy.GetParameterAsText(0)
fcpubroad=arcpy.GetParameterAsText(1)
addfieldname=arcpy.GetParameterAsText(2)

arcpy.AddField_management(fcpubroad,"larea","FLOAT")

fieldexpression="!shape.area!"
arcpy.CalculateField_management (fcpubroad, "larea" , fieldexpression ,"PYTHON_9.3")

targetFeatures = fcparcel
joinFeatures = fcpubroad
  
# Create a new fieldmappings and add the two input feature classes.
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(targetFeatures)
fieldmappings.addTable(joinFeatures)
 
buareaFieldIndex = fieldmappings.findFieldMapIndex("larea")
fieldmap = fieldmappings.getFieldMap(buareaFieldIndex)
 
# Get the output field's properties as a field object
field = fieldmap.outputField
 
# Rename the field and pass the updated field object back into the field map
field.name = "sumlarea"
fieldmap.outputField = field
 
# Set the merge rule to mean and then replace the old fieldmap in the mappings object
# with the updated one
fieldmap.mergeRule = "sum"
fieldmappings.replaceFieldMap(buareaFieldIndex, fieldmap)
 
# Remove all output fields from the field mappings, except fields "Street_Class", "Street_Name", & "Distance"
for field in fieldmappings.fields:
    if field.name not in ["FID","sumlarea"]:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))
 
#Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, tempData, "#", "#", fieldmappings)

    
arcpy.JoinField_management(fcparcel, "FID", tempData, "TARGET_FID", ["sumlarea"])
arcpy.AddField_management(fcparcel,addfieldname,"FLOAT")




fieldexpression="!sumlarea!/!shape.area!"
arcpy.CalculateField_management (fcparcel, addfieldname , fieldexpression ,"PYTHON_9.3")

arcpy.DeleteField_management(fcparcel, "sumlarea")

arcpy.Delete_management(tempData)


