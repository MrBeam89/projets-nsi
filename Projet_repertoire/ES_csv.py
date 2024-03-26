################################################################################
#  Gestion de repertoire téléphonique avec lecture/ecriture au format ²
#   et entrées au format : {"Nom" : "Numéro"}
##################################################

import csv

## Fonctions de lecture et ecriture d'un repertoire (dictionnaire) dans un fichier csv

def read_rep(nomf:str)->dict:
    """
read_rep(nomf:str)->dict
Retourne le reperoire contenu dans le fichier nomf.csv sous forme de dictionnaire
    """
    rep={}
    # Ouverture du fichier nomf.csv en lecture
    myfile = open(nomf,'rt', encoding="utf-8")
    myrep=csv.reader(myfile, delimiter=';', dialect='excel', lineterminator='\n')
    # lecture du fichier
    for row in myrep:
        rep[row[0]]=[row[1],row[2],row[3]]
    # Fermeture du fichier
    myfile.close()

    return rep

def write_rep(rep:dict,nomf:str)-> None:
    """
write_rep(rep:dict,nomf:str)->None
Verse le contenu du repertoite rep (dictionnaire) dans le fichier nomf.csv
    """
    # Ouverture du fichier nomf.csv en écriture
    myfile = open(nomf,'w', encoding="utf-8")
    mywriter = csv.writer(myfile, delimiter=';', dialect='excel', lineterminator='\n')

    # Ecriture du fichier
    for n,t in rep.items():
        mywriter.writerow([n,t[0],t[1],t[2]])

    # fermeture du fichier
    myfile.close()


## Fonctionnalités






