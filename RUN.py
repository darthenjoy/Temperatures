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
filename2 = 'TEMPDS'

# ajout sondes DS18B20
sensorids = ["28-0000065be725" , "28-0000065cc304" , ]
# Je liste les offsets des capteurs ici (en degres celcius (ecart entre valeur lue et valeur reelle)
sensoroffset = [0.00 , 0.00]

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
dataset2 = {}
# Generer un timestamp serialisable (format RfC 3339)
timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
dataset["timestamp"] = timestamp
dataset2["timestamp"] = timestamp
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

# Creation d'une liste de temperatures moyennees
avgtemperatures = []
# Boucle pour chaque capteur
for sensor in range(len(sensorids)):
	# Creation d'une liste des temperatures instantanees
	iter = 0
	temperatures = []
	# Faire 5 mesures pour chaque capteur
	for lloop in range(0,6):
			text = '';
			# Lecture de chaque capteur si CHECKSUM OK et a intervalle d'une demi seconde
			while text.split("\n")[0].find("YES") == -1:
					try:
						tfile = open("/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave")
					# Elimine donnees si un capteur de la liste est deconnecte
					except IOError:
						text = 'NO DATA. YES'
						# N'affiche qu'une erreur par sonde pas 6
						if iter == 0 : print 'sensor '+str(sensor)+' is missing or failing. Poll Loop '+str(lloop)
						iter += 1
					else:	
						text = tfile.read()
						tfile.close()
						time.sleep(0.5)
 
			if text != 'NO DATA. YES':
				secondline = text.split("\n")[1]
				temperaturedata = secondline.split(" ")[9]
				# Conversion en degres car le capteur donne une valeur en millidegres
				temperature = round(float(temperaturedata[2:])/1000 - sensoroffset[sensor],2)
			else: 
				# Temperature en cas de capteur manquant : -99 degres
				temperature = -99
			# Ajout a la liste de valeurs
			temperatures.append(temperature)
			# Affichage avec valeur de temperature arrondie a 2 chiffres apres la virgule

	# Eliminer les 2 temperatures les plus extremes (eliminer les deltas de lecture)
	temperatures = sorted(temperatures)
        del temperatures[5]
        del temperatures[0]
	# print "liste des temperatures retenues", temperatures
	
	# Calcul de la moyenne et enregistrement avec arrondi a 2 chiffres apres la virgule
	moyenne = round(sum(temperatures) / float(len(temperatures)),2)
	#print 'moyenne='+str(moyenne)
	if moyenne == -99:
		# Cas d'un capteur manquant : valeur = null
		moyenne = None
	avgtemperatures.append(moyenne)

for sensor in range (len(sensorids)):
        dataset2["temp_sensor_"+str(sensor)] = []
for sensor in range (len(sensorids)):
	# print 'Sensor '+str(sensor)
	# print 'Avg value '+str(avgtemperatures[sensor])
	dataset2["temp_sensor_"+str(sensor)].append(avgtemperatures[sensor])
# ouvrir le fichier JSON configure en debut de script en mode append
with open(foldername+filename2+'.JSON', 'a') as fichierjson:
	json.dump(dataset2, fichierjson, indent=4)

# ecrire aussi dans un fichier texte en format plus brut
# Formats datetime to a JavaScript date timestamp (milliseconds since Jan 1st 1970)
with open(foldername+filename2+'.TXT', 'a') as fichiertxt2:
	fichiertxt2.write('['+str(js_timestamp))
	for sensor in range (len(sensorids)):
		if avgtemperatures[sensor] != None:
	        	fichiertxt2.write(','+str(avgtemperatures[sensor]))
		else:
			fichiertxt2.write(',0')
	fichiertxt2.write(','+str(moyennetemp))
	fichiertxt2.write('],')	
#print(dataset)
print(json.dumps(dataset2))
