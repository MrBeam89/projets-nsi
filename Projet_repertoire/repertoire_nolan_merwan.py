import ES_csv

CSV_FILENAME = "test2"

# Initialiser le répertoire
def init_rep(filename):
    # Essaye d'ouvrir le répertoire en format CSV. S'il n'existe pas, créé un nouveau répertoire
    try:
        donnees = ES_csv.read_rep(CSV_FILENAME)
        return donnees
    except FileNotFoundError:
        ES_csv.write_rep({}, CSV_FILENAME) # Créé un répertoire vide
        return {}
    except Exception as e: # En cas d'autres erreurs
        print(e)
        exit()

# Mettre à jour le répertoire
def update_rep(repertoire):
    ES_csv.write_rep(repertoire, CSV_FILENAME)
    repertoire = ES_csv.read_rep(CSV_FILENAME)

# Lister les entrées
def list_rep(repertoire):
    for entree in repertoire.keys():
        print(f"{entree} : {repertoire[entree]}")
    return None

# Ajouter une entrée au répertoire
def add_rep(repertoire, nom, numero):
    if not numero.strip().isdigit(): return None
    repertoire[nom] = numero
    repertoire = update_rep(repertoire)

# Supprimer une entrée du répertoire
def rem_rep(repertoire, nom):
    del repertoire[nom]
    repertoire = update_rep(repertoire)

# Rechercher numéro d'après le nom
def find_number(repertoire, nom):
    print("Non-implémenté")

# Rechercher nom d'après le numéro
def find_name(repertoire, numero):
    print("Non-implémenté")

repertoire = init_rep(CSV_FILENAME)
print(repertoire)
list_rep(repertoire)