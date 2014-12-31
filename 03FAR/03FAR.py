
'''
Created on 2014.10.12
@author: xiaogelunbu


'''


import arcpy


fc2=arcpy.GetParameterAsText(0)
fieldbuarea=arcpy.GetParameterAsText(1)
fieldlarea=arcpy.GetParameterAsText(2)
addfieldname2=arcpy.GetParameterAsText(3)

arcpy.env.workspace = fc2
arcpy.AddField_management(fc2,addfieldname2,"FLOAT")


fieldexpression="!"+fieldbuarea+"!/!"+fieldlarea+"!"
arcpy.CalculateField_management (fc2, addfieldname2, fieldexpression ,"PYTHON_9.3")



    