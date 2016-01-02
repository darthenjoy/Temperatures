# Script Python pour la lecture des multiples sondes AM2302 temperature et humidite
import sys
import Adafruit_DHT
import os
import glob
import time
import datetime
import json

# Emplacement du fichier JSON d'enregistrement des mesures
foldername = '/mnt/rasponline/'
# Nom de fichier sans extension (la mettra tout seul)
filename = 'TEMP3'

# Je liste les offsets des capteurs ici (en degres celcius (ecart entre valeur lue et valeur reelle)
sensoroffset = [0.00 , 0.00]

# definition des listes de valeurs des sondes
listtemp = list()
listhum = list()
Error = 0

# lecture six fois des valeurs BMP180 et SI1145 et stockage en listes
for pollloop in range(0,15) :
	humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.AM2302, 4)
	if humidity is not None and temperature is not None:
		listtemp.append(temperature)
		listhum.append(humidity)
	else:
		Error += 1
		print 'Error reading', Error
	time.sleep(2)

# tri des listes
listtemp = sorted(listtemp)
listhum = sorted(listhum)		
print listtemp, listhum

# suppression des valeurs extremes	
# del listtemp[14]
# del listtemp[0]
# del listhum[14]
# del listhum[0]

if len(listtemp) is None:
	sys.exit()
else:
	# calcul des moyennes
	moyennetemp = round(sum(listtemp) / float(len(listtemp)),1)
	moyennehum = round(sum(listhum) / float(len(listhum)),1)

	# Enregistrer le timestamp et afficher les valeurs
	from datetime import datetime

	# Ecriture des donnees timestamp et valeurs de temperature dans un fichier JSON
	dataset = {}
	# Generer un timestamp serialisable (format RfC 3339)
	timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	dataset["timestamp"] = timestamp
	dataset["temp"] = moyennetemp
	dataset["humidity"] = moyennehum


	# ouvrir le fichier JSON configure en debut de script en mode append
	with open(foldername+filename+'.JSON', 'a') as fichierjson:
		json.dump(dataset, fichierjson, indent=4)

	# ecrire aussi dans un fichier texte en format plus brut
	# Formats datetime to a JavaScript date timestamp (milliseconds since Jan 1st 1970)
	import datetime, time
	d = datetime.datetime.now()
	js_timestamp = int(time.mktime(d.timetuple())) * 1000
	with open(foldername+filename+'.TXT', 'a') as fichiertxt:
		fichiertxt.write('['+str(js_timestamp))
		fichiertxt.write(','+str(moyennetemp))
		fichiertxt.write(','+str(moyennehum))
		fichiertxt.write('],')	

	#print(dataset)
	print(json.dumps(dataset))

