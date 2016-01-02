# Script Python pour la lecture de multiples sondes SI1145 et BMP180
import os 
import glob 
import time
import datetime
import json
import Adafruit_BMP.BMP085 as BMP085
import SI1145.SI1145 as SI1145

# Emplacement du fichier JSON d'enregistrement des mesures
foldername = '/mnt/rasponline/'
# Nom de fichier sans extension (la mettra tout seul)
filename = 'TEMP1'

# ajout sonde BMP180
bmp = BMP085.BMP085()

# ajout sonde SI1145
sensor = SI1145.SI1145()

# definition des listes de valeurs des sondes
listtemp = list()
listpressure = list()
listaltitude = list()
listvis = list()
listIR = list()
listUV = list()
listuvIndex = list()

# lecture six fois des valeurs BMP180 et SI1145 et stockage en listes
for pollloop in range(0,6) :
	temp = bmp.read_temperature()
	listtemp.append(temp)
	pressure = bmp.read_pressure()
	listpressure.append(pressure)
	altitude = bmp.read_altitude()
	listaltitude.append(altitude)
	vis = sensor.readVisible()
	listvis.append(vis)
	IR = sensor.readIR()
	listIR.append(IR)
	UV = sensor.readUV()
	listUV.append(UV)
	# Calcul de la valeur uvIndex de la sonde SI1145 et stockage en liste
	uvIndex = UV / 100.0
	listuvIndex.append(uvIndex)
	time.sleep(0.5)

		
# suppression des valeurs extremes	
del listtemp[5]
del listtemp[0]
del listaltitude[5]
del listaltitude[0]
del listpressure[5]
del listpressure[0]
del listvis[5]
del listvis[0]
del listIR[5]
del listIR[0]
del listUV[5]
del listUV[0]
del listuvIndex[5]
del listuvIndex[0]

# tri des listes
listtemp = sorted(listtemp)
listpressure = sorted(listpressure)
listaltitude = sorted(listaltitude)
listvis = sorted(listvis)
listIR = sorted(listIR)
listUV = sorted(listUV)
listuvIndex = sorted(listuvIndex)
		
# calcul des moyennes
moyennetemp = round(sum(listtemp) / float(len(listtemp)),1)
moyennepressure = int(sum(listpressure) / float(len(listpressure)))
moyennealtitude = round(sum(listaltitude) / float(len(listaltitude)),9)
moyennevis = int(sum(listvis) / float(len(listvis)))
moyenneIR = int(sum(listIR) / float(len(listIR)))
moyenneUV = int(sum(listUV) / float(len(listUV)))
moyenneuvIndex = round(sum(listuvIndex) / float(len(listuvIndex)),2)


# Enregistrer le timestamp et afficher les valeurs
from datetime import datetime

# Ecriture des donnees timestamp et valeurs de temperature dans un fichier JSON
dataset = {}
# Generer un timestamp serialisable (format RfC 3339)
timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
dataset["timestamp"] = timestamp

# dataset BMP180
dataset["pression"] = moyennepressure
dataset["altitude"] = moyennealtitude
dataset["temp"] = moyennetemp
# dataset SI1145
dataset["vis"] = moyennevis
dataset["IR"] = moyenneIR
dataset["UV"] = moyenneUV
dataset["uvIndex"] = moyenneuvIndex


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
	fichiertxt.write(','+str(moyennepressure))
	fichiertxt.write(','+str(moyennealtitude))
	fichiertxt.write(','+str(moyennetemp))
	fichiertxt.write(','+str(moyennevis))
	fichiertxt.write(','+str(moyenneIR))
	fichiertxt.write(','+str(moyenneUV))
	fichiertxt.write(','+str(moyenneuvIndex))

	fichiertxt.write('],')	

#print(dataset)
print(json.dumps(dataset))
