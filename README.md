# clipping vector  graphics for remote sensing

This script implements a projection and then a clip 
	between two vector graphics using gdal library. 
	The complete workflow can take several hours
    if there are a lot of vector graphs to processes. 
 	It is essential that alongside the *.shp files 
 	also may be files with extensions *.dbf, *.prj, and *.shx. 

 	Example: python clippingVector.py /path/to/shapeFather path/to/shapeSon /path/to/output file_output option_reproj
    option_reproj: 0 No projection
    option_reproj: 1 computes the projection processes 
