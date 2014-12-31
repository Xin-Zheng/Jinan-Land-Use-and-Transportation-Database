Jinan-Land-Use-and-Transportation-Database (Planning support systems)
==========================================

This repo is an toolbox that supports planning decision and help to analyze relationship between land use and transportation

What Indexs This Toolbox Calculate 
------------------------
26 in 1

01Land-Area
02Building-Area
03FAR
04Building-Density
05Land-Use-Mix1
06Land-Use-Mix2
07PublicRoad-Ratio
08Road-Density
09Road-Area
10City-Accessibility1
11Green-Ratio
12Road-Setback
13SETBACKparcel
14Height-Width-Ratio
15Road-Grenn-Shade
16Road-Retail-Ratio
18Road-Right-Mix
19Curb-Park
20Illegal-Park
21FrontPark
22RoadWidth
23Crossing-Density
24Busstop-Density
25City-Accessibility2
26Crossing-Number


How This Solves It
------------------
This repo is two components that work inside ESRI ArcGIS.  First it is a python script that works at the lowest ESRI software license level.  Second, this repo has an ESRI toolbox (or .tbx file) that allows any ESRI user to easily connect this python script to native ESRI software.  The toolbox points at the script.  Users of this software need both files (the .tbx and the .py) to operate these functions.  Once these files are download, just add the .tbx file to the normal ESRI toolbox and run the .py script by double clicking on the script icon in the toolbox.

Requirements
------------
Runs inside the ESRI ArcGIS desktop suite.

Usage
------
1. Copy the .tbx file and the .py file to any local directory
2. With ArcGIS desktop software running (e.g. ArcCatalog), add the .tbx file to your tool box by right clicking and choosing 'Add Toolbox'.
3. Double click on the which script you want to run which are

License
-------
MIT

Issues
------
* Need to work on error trapping a bit more
* This does not handle blob fields, or raster fields
* Need to document python version; not sure how compatible it is with all current versions
* Developed in ArcGIS 10.0
