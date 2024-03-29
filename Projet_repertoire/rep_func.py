"""
Fichier : rep_func.py
Date de création : 27 mars 2024
Description : Module contenant les fonctions pour effectuer des opérations sur un répertoire sous forme de fichier CSV
"""

import ES_csv

def init_rep(filename:str)->dict:
    '''
    Initialiser le répertoire à partir d'un fichier CSV déjà existant ou en créer un si le fichier n'existe pas
    Obligatoire pour utiliser les autres fonctions (stocke le chemin d'accès de façon permanente pour éviter redondance)

    Paramètres :
    filename (str) : Chemin d'accès du fichier

    Renvoie :
    donnees (dict): Données du répertoire

    Exemple :
    Soit un fichier "repertoire.csv" situé dans le répertoire actuel
    Foo;123;foo@bar.com;★
    Spam;456;spam@eggs.com;

    >>> repertoire = init_rep("repertoire.csv")
    >>> print(repertoire)
    {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    '''

    global _csv_filename                    # Variable permanente pour stocker le chemin d'accès au fichier
    try:                                    # Essayer de...
        donnees = ES_csv.read_rep(filename) # Lire les données du fichier à partir du chemin donné
        _csv_filename = filename            # Stocker le chemin du fichier de façon permanente
        return donnees                      # Renvoyer les données du répertoire (en dictionnaire)
    except FileNotFoundError:               # Mais si le fichier n'existe pas
        ES_csv.write_rep({}, filename)      # Créer un répertoire (fichier) vide
        _csv_filename = filename            # Stocker le chemin du fichier de façon permanente
        return {}                           # Renvoyer un dictionnaire vide
    except Exception as e:                  # Mais si d'autres erreurs se produisent
        print(e)                            # Afficher un message d'erreur
        exit()                              # Arrêter l'exécution


def save_rep(repertoire:dict)->None:
    '''
    Enregistrer le répertoire (modifié ou pas)

    Paramètres:
    repertoire (dict) : Répertoire

    Renvoie :
    None
    '''

    ES_csv.write_rep(repertoire, _csv_filename)


def add_edit_rep(repertoire:dict, nom:str, numero:str, email:str, favori:str)->None:
    '''
    Ajouter ou modifier une entrée du répertoire

    Arguments :
    repertoire (dict) : Répertoire
    nom (str) : Nom
    numero (str) : Numéro de téléphone
    email (str) : Adresse e-mail
    favori (str) : '★' ou '' (oui/non)

    Renvoie :
    None

    Exemple :
    >>> # Ajouter une entrée
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"]} # Possible d'utiliser init_rep()
    >>> add_edit_rep(repertoire, "Spam", "456", "spam@eggs.com", "")
    >>> print(repertoire)
    {"Spam": ["456", "spam@eggs.com", ""]}

    >>> # Modifier une entrée
    >>> add_edit_rep(repertoire, "Foo", "789", "foo.bar@baz.com", "")
    >>> print(repertoire)
    {"Foo": ["789", "foo.bar@baz.com", ""], "Spam": ["456", "spam@eggs.com", ""]}
    '''

    nom = str(nom)                     # Fix pour nom contenant que des chiffres
    repertoire[nom] = ['', '', '', ''] # Si entrée non existante -> Ajouter l'entrée (sinon écraser les données)
    repertoire[nom][0] = numero        # Ajouter/modifier le numéro
    repertoire[nom][1] = email         # Ajouter/modifier l'e-mail
    repertoire[nom][2] = favori        # Ajouter/modifier si favori ou non


def rem_rep(repertoire:dict, nom:str)->None:
    '''
    Supprimer une entrée du répertoire avec le nom

    Arguments :
    repertoire (dict) : Répertoire
    nom (str) : Nom

    Renvoie :
    None

    Exemple :
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    >>> rem_rep(repertoire, "Foo")
    >>> print(repertoire)
    {"Spam": ["456", "spam@eggs.com", ""]}
    '''

    nom = str(nom)      # Fix pour nom contenant que des chiffres
    del repertoire[nom] # Supprimer l'entrée du dictionnaire


def search_name(repertoire:dict, nom:str)->dict:
    '''
    Chercher toutes les entrées dans le répertoire dont le nom contient une chaîne de caractères donnée

    Arguments :
    repertoire (dict) : Répertoire
    nom (str) : Nom

    Renvoie :
    resultat (dict) : Résultat de la recherche contenant les entrées correspondantes
    
    Exemple :
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    >>> recherche = search_name(repertoire, "F")
    >>> print(recherche)
    {"Foo": ["123", "foo@bar.com", "★"]}
    '''

    resultat = {}                          # Créer le dictionnaire des recherches
    nom = str(nom)                         # Fix pour nom contenant que des chiffres
    for cle, valeur in repertoire.items(): # Pour chaque entrée dans le répertoire
        if nom in cle:                     # Si le nom de l'entrée contient la chaîne donnée
                resultat[cle] = valeur     # Rajouter cette entrée au dictionnaire des résultats
    return resultat                        # Renvoyer le résultat


def search_number(repertoire:dict, numero:str)->dict:
    '''
    Chercher toutes les entrées dans le répertoire dont le nom contient une chaîne de caractères (contenant des chiffres) donnée

    Arguments :
    repertoire (dict) : Répertoire
    numero (str) : Numéro de télélphone

    Renvoie :
    resultat (dict) : Résultat de la recherche contenant les entrées correspondantes
    
    Exemple :
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    >>> recherche = search_number(repertoire, "45")
    >>> print(recherche)
    {"Spam": ["456", "spam@eggs.com", ""]}
    '''

    resultat = {}
    for cle, valeur in repertoire.items(): # Pour chaque entrée dans le répertoire
        if numero in valeur[0]:            # Si le numéro de l'entrée contient les chiffres donnés
            resultat[cle] = valeur         # Afficher l'entrée (élément 0 : nom; élément 1 : numéro)
    return resultat


def search_email(repertoire:dict, email:str)->dict:
    '''
    Chercher toutes les entrées dans le répertoire dont l`e-mail contient une chaîne de caractères donnée

    Arguments :
    repertoire (dict) : Répertoire
    email (str) : E-mail

    Renvoie :
    resultat (dict) : Résultat de la recherche contenant les entrées correspondantes
    
    Exemple :
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    >>> recherche = search_email(repertoire, "foo@")
    >>> print(recherche)
    {"Foo": ["123", "foo@bar.com", "★"]}
    '''

    resultat = {}                          # Créer le dictionnaire des recherches
    for cle, valeur in repertoire.items(): # Pour chaque entrée dans le répertoire
        if email in valeur[1]:             # Si l'e-mail de l'entrée contient la chaîne donnée
            resultat[cle] = valeur         # Rajouter cette entrée au dictionnaire des résultats
    return resultat                        # Renvoyer le résultat


def search_favorite(repertoire:dict, est_favori:bool)->dict:
    '''
    Chercher toutes les entrées dans le répertoire qui font parti des favoris (ou pas)

    Arguments :
    repertoire (dict) : Répertoire
    est_favori (bool) : Favori ou non-favori (True/False)

    Renvoie :
    resultat (dict) : Résultat de la recherche contenant les entrées correspondantes
    
    Exemple :
    >>> repertoire = {"Foo": ["123", "foo@bar.com", "★"], "Spam": ["456", "spam@eggs.com", ""]}
    >>> recherche = search_email(repertoire, False)
    >>> print(recherche)
    {"Spam": ["456", "spam@eggs.com", ""]}
    '''

    resultat = {}                          # Créer le dictionnaire des recherches
    for cle, valeur in repertoire.items(): # Pour chaque entrée dans le répertoire
        if bool(valeur[2]) == est_favori:  # Si l'entrée est favori/ne l'est pas (selon argument)
            resultat[cle] = valeur         # Rajouter cette entrée au dictionnaire des résultats
    return resultat                        # Renvoyer le résultat
