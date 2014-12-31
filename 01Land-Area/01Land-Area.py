'''
Created on 2014.10.12
@author: xiaogelunbu



'''

# Name: CalculateField_Centroids.py
# Description: Use CalculateField to assign centroid values to new fields

#-*-coding:cp936-*-
# Import system modules
import arcpy

# Set environment settings
fc=arcpy.GetParameterAsText(0)
addfieldname=arcpy.GetParameterAsText(1)

arcpy.AddField_management(fc,addfieldname,"FLOAT")

fieldexpression="!shape.area!"
arcpy.CalculateField_management (fc, addfieldname, fieldexpression,"PYTHON_9.3")



    