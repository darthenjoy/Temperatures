#!/usr/bin/env python
# Script Python pour la recherche de valeurs min et max sur une periode
import sys
import getopt
import os 
import glob 
import time
import datetime

foldername = '/mnt/rasponline/'
# Rechercher des temp. min et max su les dernieres 24h
# sensorid = 2 		# numero du capteur concerne
# timeframe = 24	# nombre d'heures a considerer pour la periode d'analyse

#------------------------------------------------------------------------------------------
# Example GETMINMAX.py 2 24 /var/www/TEMP2b.TXT
def main(argv):

	#initialisation des variable
	sensorid = 0
	timeframe = 0
	filename = ''

#        print 'a sensorid ='+str(sys.argv[1])
#        print 'a timeframe ='+str(sys.argv[2])
#        print 'a filename ='+str(sys.argv[3])

	try:
		opts, args = getopt.getopt(argv,"h","help")
	except getopt.GetoptError:
		print 'usage: GETMINMAX.py sensorid nbhours sourcefile'
	      	sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h', '-help'):
      			print 'usage: GETMINMAX.py sensorid nbhours sourcefile'
         		sys.exit()
#		else:
#			sensorid = int(str(sys.argv[1]))
#		        timeframe = int(str(sys.argv[2]))
#        		filename = foldername+str(sys.argv[3])
#    			print 'b sensorid ='+str(sensorid)
#        		print 'b timeframe ='+str(timeframe)
#        		print 'b filename ='+filename
			
        sensorid = int(str(sys.argv[1]))
        timeframe = int(str(sys.argv[2]))
        filename = foldername+str(sys.argv[3])


	import datetime, time 

#	print 'c sensorid ='+str(sensorid)
#	print 'c timeframe ='+str(timeframe)
#	print 'c filename ='+filename

	d = datetime.datetime.now() 
	js_timestamp_now = int(time.mktime(d.timetuple())) * 1000 
	js_timestamp_start = js_timestamp_now - timeframe * 3600000
	#print (js_timestamp_start)

	foundmin = 999
	foundmax = -999
	with open(filename, 'r') as database:
		for entry in database:
			if len(entry) > 13: # Elimine les eventuelles entrees trop courtes
#				print entry 
				value = entry.split(',')
				try:
				    	timestamp = int(value[0][1:14])
				except ValueError:
#					print 'error:' + value[0]
				    	timestamp = 0
			if timestamp > js_timestamp_start:
				if float(value[sensorid]) > foundmax:
					foundmax = float(value[sensorid])
					#print 'max:'+str(foundmax)
				if float(value[sensorid]) < foundmin:
	                                foundmin = float(value[sensorid])
					#print 'min:'+str(foundmin)
	print str(foundmax)+';'+str(foundmin)
	database.close()

if __name__ == "__main__":
	main(sys.argv[1:])

