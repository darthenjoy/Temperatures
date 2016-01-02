# PARSER pour ajouter des \n en fin de chaque entree pour les fichiers HighCharts et HighStock !/usr/bin/env python
import shutil

# ORIGINE
# Emplacement du fichier JSON d'enregistrement des mesures
foldernameORIG = '/mnt/rasponline/'
filenameORIG = 'TEMPDS2.TXT'

# DESTINATION
# Emplacement du fichier JSON d'enregistrement des mesures
foldernameDEST = '/mnt/rasponline/'
filenameDEST = 'TEMPDS2b.TXT'

# ecrire dans un fichier texte portant le nouveau nom et ajouter un '\n,' apres chaque '],'
fichierORIG = open(foldernameORIG+filenameORIG, 'r')
fichierDEST = open(foldernameDEST+filenameDEST, 'w')
begin_balise = '['
end_balise1 = ']'
end_balise2 = ','

fichierORIG.seek(0,2) # move the cursor to the end of the file
taille = fichierORIG.tell()
fichierORIG.seek(0,0) # move the cursor to the start of the file

i=0
while i < taille:
	i += 1
	char = fichierORIG.read(1)
	fichierDEST.write(char)
	if char == end_balise1:
		char2 = fichierORIG.read(1)
		fichierDEST.write(char2)
		if char2 == end_balise2:
			fichierDEST.write('\n')
#			print '---'+str(i)
fichierDEST.close()
