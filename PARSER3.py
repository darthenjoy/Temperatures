# PARSER pour actualiser fichiers pour HighCharts et HighStock
#!/usr/bin/env python
import shutil

# ORIGINE
# Emplacement du fichier JSON d'enregistrement des mesures
foldernameORIG = '/mnt/rasponline/'
filenameORIG = 'EDF1.TXT'

# DESTINATION
# Emplacement du fichier JSON d'enregistrement des mesures
foldernameDEST = '/mnt/rasponline/'
filenameDEST = 'EDF2.TXT'

shutil.copyfile(foldernameORIG+filenameORIG, foldernameDEST+filenameDEST)

# ecrire dans un fichier texte portant le nouveau nom et remplacer le dernier ',' par ']'
fichierDEST = open(foldernameDEST+filenameDEST, 'r+')
# Seek to the end. (1 byte relative to the end)
fichierDEST.seek(-1, 2)
#length = file.tell()
fichierDEST.write (']')

