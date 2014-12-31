'''
Created on 20141024

@author: xiaogelunbu
'''

import arcpy
import os

arcpy.env.overwriteOutput=True


fcpubroad="C:/jiefang0827/pubroadclip.shp"
widthfield="width"
buildpoint="C:/jiefang0827/shangyepoi.shp"
widthinput="20"
addfieldname="set"


arcpy.DeleteField_management(fcpubroad,"searchwid")
arcpy.AddField_management(fcpubroad,"searchwid","FLOAT")

widthnum=float(widthinput)
cur = arcpy.UpdateCursor(fcpubroad)
for row in cur: 
    row.setValue("searchwid", row.getValue(widthfield)+widthnum*2)
    cur.updateRow(row)


tempbuffer = "C:/jiefang0827/buffer.shp"
widthinnum=float(widthinput)
arcpy.Buffer_analysis(fcpubroad,tempbuffer,"searchwid","#","FLAT","#","#")
arcpy.Near_analysis (buildpoint, fcpubroad)

def spatialjoinmean(intar,injoin,infieldname,outfieldname,jointype):
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
    fieldmap.mergeRule = "mean"
    fieldmappings.replaceFieldMap(FieldIndex, fieldmap)
 
    # Remove all output fields from the field mappings, except fields "Street_Class", "Street_Name", & "Distance"
    for field in fieldmappings.fields:
        if field.name not in ["FID",outfieldname,"NEAR_DIST"]:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))
 
    #Run the Spatial Join tool, using the defaults for the join operation and join type
    arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, tempData, "#", "#", fieldmappings,jointype)
    arcpy.DeleteField_management(intar, outfieldname)
    arcpy.JoinField_management(intar, "FID", tempData, "TARGET_FID", [outfieldname])
    arcpy.Delete_management(tempData)

spatialjoinmean(tempbuffer,buildpoint,"NEAR_DIST",addfieldname,"CONTAINS")

arcpy.JoinField_management(fcpubroad, "FID", tempbuffer, "FID", [addfieldname])

arcpy.Delete_management(tempbuffer)





