#!/usr/bin/env python
# -*- coding: utf-8
 
   
'''
	Created on 29.04.2016
	@author: rmartinez

'''


''' This script implements a projection and then a clip 
	between two vector graphics using gdal library. 
	The complete workflow can take several hours
    if there are a lot of vector graphs to processes. 
 	It is essential that alongside the *.shp files 
 	also may be files with extensions *.dbf, *.prj, and *.shx. 


    Example: python clippingVector.py /path/to/shapeFather path/to/shapeSon /path/to/output file_output option_reproj
    option_reproj: 0 No projection
    option_reproj: 1 computes the projection processes
'''

import logging 
import subprocess
import shlex
import time
import os
import multiprocessing
import sys




def removeFinishedProcesses(processes):

    '''
    	Given a list of (commandString, process), 
        remove those that have completed and return the result 
    '''
    newProcs = []
    for pollCmd, pollProc in processes:
        retCode = pollProc.poll()
        if retCode==None:
            # still running
            newProcs.append((pollCmd, pollProc))
        elif retCode!=0:
            # failed
            raise Exception("Command %s failed" % pollCmd)
        else:
            logging.info("Command %s completed successfully" % pollCmd)
    
    return newProcs


def runCommands(commands, maxCpu):

            processes = []
            for command in commands:
                logging.info("Starting process %s" % command)
                logging.getLogger().setLevel(logging.INFO)
                proc =  subprocess.Popen(shlex.split(command))
                procTuple = (command, proc)
                processes.append(procTuple)
                while len(processes) >= maxCpu:
                    time.sleep(.2)
                    processes = removeFinishedProcesses(processes)


            # wait for all processes
            while len(processes)>0:
                time.sleep(0.5)
                processes = removeFinishedProcesses(processes)
            logging.info("All processes completed")


def main (path_shapeFather, path_shapeSon, path_output, file_output, option_reproj):

	cores = multiprocessing.cpu_count()
	
	# Empty list for files 
	lstFiles = []
 
	# List with all distinct file extensions in folder 
	lstDir = os.walk(path_shapeFather)  
 
 
	# List with *.shp files 
 
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = os.path.splitext(fichero)
			if(extension == ".shp"):
				lstFiles.append(nombreFichero+extension)
				print 'Shape file to use: ', nombreFichero+extension


	if option_reproj == 1:
		# Projections 
		print 'projecting'
		projection_commands = []
		
		for shapeFile in lstFiles:
		 	projection_commands.append('ogr2ogr -t_srs EPSG:4326 ' + 'rep_' + str(shapeFile) + ' ' + path_shapeFather + str(shapeFile))
		 	print projection_commands
		runCommands(projection_commands, cores)


	# Clip
	# It is mandatory to use the projected file 
	print 'clipping'
	clip_commands = []
	for i in range(len(lstFiles)):
		infile = str (lstFiles[i])
		no_ext = infile.split('.')
		clip_commands.append('ogr2ogr -progress -clipsrc '+ str(path_shapeSon) + ' ' + str(path_output) + '/' + str(no_ext[0]) + '_'+ str(file_output) + '.shp' + ' ' + 'rep_' + str(infile))
		
	runCommands(clip_commands, cores)


if __name__ == '__main__':
	
	main( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) )














