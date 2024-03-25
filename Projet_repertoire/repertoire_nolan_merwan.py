import ES_csv

# Initialiser le répertoire
def init_rep(filename):
    # Essaye d'ouvrir le répertoire en format CSV. S'il n'existe pas, créé un nouveau répertoire
    global csv_filename
    try:
        donnees = ES_csv.read_rep(filename)
        csv_filename = filename
        return donnees
    except FileNotFoundError:
        ES_csv.write_rep({}, filename) # Créé un répertoire vide
        csv_filename = filename
        return {}
    except Exception as e: # En cas d'autres erreurs
        print(e)
        exit()

# Sauvegarder le répertoire
def save_rep(repertoire):
    ES_csv.write_rep(repertoire, csv_filename)

# Lister les entrées
def list_rep(repertoire):
    for entree in repertoire.keys():
        print(f"{entree} : {repertoire[entree]}")
    return None

# Ajouter/modifier une entrée du répertoire
def add_edit_rep(repertoire, nom, numero, email, favori):
    repertoire[nom] = ['', '', '', ''] # Si entrée non existante -> Ajouter l'entrée
    repertoire[nom][0] = numero        # Modifie le numéro
    repertoire[nom][1] = email         # Modifie l'e-mail
    repertoire[nom][2] = favori        # Modifie si favori ou non

# Supprimer une entrée du répertoire
def rem_rep(repertoire, nom):
    del repertoire[nom]

# Rechercher numéro d'après le nom
def find_number(repertoire, nom):
    for entree in repertoire.items():           # Pour chaque entrée dans le répertoire
        if entree[0].startswith(nom):           # Si le nom de l'entrée commence par les caractères donnés
            print(f"{entree[0]} : {entree[1]}") # Afficher l'entrée (élément 0 : nom; élément 1 : numéro)

# Rechercher nom d'après le numéro
def find_name(repertoire, numero):
    if not numero.isdigit(): return None        # Si le numéro contient autre chose que des chiffres
    for entree in repertoire.items():           # Pour chaque entrée dans le répertoire
        if entree[1].startswith(numero):        # Si le numéro de l'entrée commence par les chiffres donnés
            print(f"{entree[0]} : {entree[1]}") # Afficher l'entrée (élément 0 : nom; élément 1 : numéro)
