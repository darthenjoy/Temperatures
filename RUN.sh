#!/bin/sh
# Ce script est appele par cron toutes les 5 minutes

# Lecture des sondes DS18B20 et BMP180 (Temperature)
python /mnt/rasponline/RUN.py
python /mnt/rasponline/RUN3.py
# Mise au format du fichier
python /mnt/rasponline/PARSER.py
python /mnt/rasponline/PARSER2.py
python /mnt/rasponline/PARSER4.py
# Lecture des information EDF
#python /mnt/rasponline/edfinfo.py
# Mise au format du fichier
#python /mnt/rasponline/PARSER3.py

# Ecriture du fichier pour recherche min max
python /mnt/rasponline/CUTLINES.py
