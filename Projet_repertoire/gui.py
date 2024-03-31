"""
Fichier : gui.py
Date : 30/03/2024
Description : Repyrtoire (Gestion de répertoire avec GUI)
"""

from tkinter import * # GUI
from tkinter import filedialog # Pour créer/ouvrir un répertoire
from tkinter import ttk # Pour le tableau
from pygame import mixer # Pour le son
import rep_func as rep # Fonctions du répertoire
import re # Pour vérifier e-mail

# Variables modifiables dans toutes les fonctions de façon globale
global repertoire, repertoire_ouvert, changements_effectues, est_dans_recherche
repertoire_ouvert = False
changements_effectues = False
est_dans_recherche = False

# Chemins d'accès au sons
ERROR_SFX_FILEPATH = "src/win_xp_error.mp3"
WARNING_SFX_FILEPATH = "src/win_xp_warning.mp3"
INFO_SFX_FILEPATH = "src/win_xp_info.mp3"

# Initialiser le lecteur de son
mixer.init()


def email_valide_verif(email:str)->bool:
    '''
    Vérifie si une adresse e-mail est valide

    Paramètres :
    - email (str) : Adresse e-mail à vérifier

    Renvoie :
    - (bool) : Adresse e-mail valide/non-valide (True/False)
    '''

    motif = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' # Motif d'expression régulière pour une adresse e-mail valide
    return re.match(motif, email) is not None # Renvoie True ou False pour une adresse valide/non-valide


def message_popup(titre:str, image_file_path:str, message:str, sound_file_path:str)->None:
    '''
    Afficher une fenêtre popup contenant un message, une image et jouant un son

    Paramètres :
    - titre (str) : Titre de la fenêtre
    - image_file_path (str) : Chemin d'accès à une image
    - message (str) : Message à afficher
    - sound_file_path (str) : Chemin d'accès au son à jouer

    Renvoie :
    None
    '''
    
    # Caractéristiques de la fenêtre
    fenetre_message_popup = Toplevel(fenetre_principale.winfo_toplevel()) # Toujours au-dessus de la fenêtre le plus au-dessus
    fenetre_message_popup.title(titre) # Titre de la fenêtre
    fenetre_message_popup.resizable(0, 0) # Taille non-modifiable
    fenetre_message_popup.grab_set() # Rendre impossible interaction avec les autres fenêtres tant que celle-ci n'est pas fermée

    # Jouer un son
    mixer.music.load(sound_file_path) # Charger le son
    mixer.music.play() # Jouer le son

    # Image
    popup_image = PhotoImage(file=image_file_path) # Ouvrir l'image à partir du chemin d'accès au fichier
    popup_image_button = Button(fenetre_message_popup, image=popup_image, command=lambda: mixer.music.play(), borderwidth=0) # Bouton-image qui joue le son lorsqu'il est cliqué
    popup_image_button.image = popup_image # Pour éviter que le ramasse-miettes de Python supprime l'image
    popup_image_button.grid(row=0, column=0, padx=(5, 0), pady=5) # Placer l'image à gauche du message sur la même ligne

    # Message
    popup_label = Label(fenetre_message_popup, text=message) # Message donné en paramètre
    popup_label.grid(row=0, column=1, padx=(0,5), pady=5) # Placer le message à droite de l'image sur la même ligne


def repertoire_ouvert_verif()->bool:
    '''
    Vérifier si un répertoire est ouvert, sinon afficher un message d'erreur

    Paramètres :
    Aucun

    Renvoie :
    - bool : Répertoire ouvert/non-ouvert (True/False)
    '''

    # Si le répertoire n'est pas ouvert
    if repertoire_ouvert == False:
        # Afficher un message d'erreur
        message_popup("Erreur", "src/error.gif", "Le répertoire n'est pas ouvert!", ERROR_SFX_FILEPATH)
        return False
    else:
        return True


def entree_selectionnee(*_)->tuple:
    '''
    Obtenir le nom de l'entrée sélectionnée et son identifiant dans le tableau

    Paramètres :
    - *_ : Aucun (ajouté pour éviter erreur)

    Renvoie:
    - (iid, name) (tuple) : Identifiant de l'entrée et son nom
    '''

    try:
        iid = entrees_tableau.focus() # Obtenir l'identifiant de l'entrée sélectionnée dans le tableau
        name = entrees_tableau.item(iid)['values'][0] # Obtenir le nom de l'entrée
    except IndexError: # Si l'en-tête du tableau est cliqué
        name = None
    finally:
        return iid, name # Renvoyer l'identifiant et le nom


def effacer_tableau_et_inserer(dic:dict)->None:
    '''
    Effacer tous les élements du tableau et insérer tous ceux dans le dictionnaire donné

    Paramètres :
    - dic (dict) : Répertoire ou résultats d'une recherche

    Renvoie :
    None
    '''

    # Supprimer toutes les entrées à l'écran
    for entree in entrees_tableau.get_children():
      entrees_tableau.delete(entree)

    # Rajouter toutes les entrées dans le dictionnaire donné
    for nom, valeur in dic.items(): # Pour chaque entrée dans le dictionnaire
        numero = valeur[0]
        email = valeur[1]
        favori = valeur[2]
        entrees_tableau.insert(parent='', index='end', text='', values=(nom, numero, email, favori)) # Insérer l'entrée dans le tableau des entrées


def nouveau_repertoire()->None:
    '''
    Créer un nouveau répertoire et le charger

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    global repertoire, filename, changements_effectues, repertoire_ouvert

    # Si des changements non-enregistrés ont été effectués
    if changements_effectues == True:
        message_popup("Avertissement", "src/warning.gif", "Des changements n'ont pas été sauvegardés!", INFO_SFX_FILEPATH)
        return

    # Obtenir un chemin d'accès au fichier à créer
    filename = filedialog.asksaveasfilename(initialfile=".csv", filetypes=[("CSV files", "*.csv")]) # Boîte de dialogue de fichier
    if not filename: return # Si la boîte de dialogue a été fermée en annulant

    # Créer le répertoire et réinitialiser le tableau des entrées
    repertoire = rep.init_rep(filename)
    effacer_tableau_et_inserer(repertoire)

    # Activer les fonctions de modification/recherche
    repertoire_ouvert = True
    changements_effectues = False


def ouvrir_repertoire()->None:
    '''
    Ouvrir un répertoire

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Si des changements non-enregistrés ont été effectués
    global repertoire, filename, changements_effectues, repertoire_ouvert
    if changements_effectues == True:
        message_popup("Avertissement", "src/warning.gif", "Des changements n'ont pas été sauvegardés!", "src/win_xp_warning.mp3")
        return

    # Obtenir le chemin d'accès au répertoire
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]) # Boîte de dialogue de fichier affichant les fichiers CSV disponibles
    if not filename: return # Si la boîte de dialogue a été fermée sans ouvrir de fichier

    # Ouvrir le répertoire, réinitialiser le tableau des entrées et insérer le contenu du répertoire dedans
    repertoire = rep.init_rep(filename)
    effacer_tableau_et_inserer(repertoire)

    # Activer les fonctions de modification/recherche
    repertoire_ouvert = True
    changements_effectues = False


def enregistrer()->None:
    '''
    Enregistrer les changements apportés au répertoire (fonctionne uniquement si répertoire ouvert)

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Vérifier qu'un répertoire est ouvert
    if not repertoire_ouvert_verif(): return

    # Si aucun changement non-enregistré
    global changements_effectues
    if changements_effectues == False:
        message_popup("Enregistrer", "src/save.png", "Aucun changement à enregistrer!", INFO_SFX_FILEPATH)
        return

    # Si changements non-enregistrés
    rep.save_rep(repertoire) # Enregistrer le répertoire dans le fichier
    message_popup("Enregistrer", "src/save.png", "Changements enregistrés!", INFO_SFX_FILEPATH) # Afficher un message via une fenêtre pop-up
    changements_effectues = False # Ne pas avertir de changement non-enregistré


def ajouter_ou_modifier_et_inserer(operation:str, iid:int, nom:str, numero:str, email:str, favori:str)->None:
    '''
    Ajouter/modifier une entrée du répertoire et l'insérer dans le tableau des entrées

    Paramètres :
    - operation (str) : "add" ou "edit" (Ajouter/modifier)
    - iid (int) : Identifiant de l'entrée dans le tableau des entrées
    - nom (str) : Nom
    - numero (str) : Numéro
    - email (str) : E-mail
    - favori (str) : '★' ou '' (Favori/non-favori)

    Renvoie :
    None
    '''

    # Enlever les espaces au début et à la fin du nom, du numéro et de l'adresse e-mail
    nom = nom.strip()
    numero = numero.strip()
    email = email.strip()

    # Si l'entrée existe déjà dans le répertoire
    if nom in repertoire and operation == "add":
        message_popup("Erreur", "src/error.gif", 'Une entrée associée à ce nom existe déjà!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter

    # Si le nom est vide
    if not nom:
        message_popup("Erreur", "src/error.gif", 'Le nom ne peut pas être vide!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter/modifier

    # Si ni le numéro ni l'email n'a été donné
    if not(numero or email):
        message_popup("Erreur", "src/error.gif", 'Pas de numéro/e-mail!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter/modifier

    # Si un numéro a été donné mais qu'il contient autre chose que des chiffres
    if numero and not numero.isdigit():
        message_popup("Erreur", "src/error.gif", 'Numéro invalide!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter/modifier

    # Si une adresse e-mail a été donnée mais qu'elle est invalide
    email = email.strip()
    if email and not email_valide_verif(email):
        message_popup("Erreur", "src/error.gif", 'E-mail invalide!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter/modifier

    # Ajouter/modifier l'entrée dans le répertoire si aucune erreur n'est détectée
    rep.add_edit_rep(repertoire, nom, numero, email, favori)

    # Si l'opération est un ajout
    if operation == "add":
        entrees_tableau.insert(parent='',index='end', text='', values=(nom, numero, email, favori)) # Ajouter l'entrée dans le tableau des entrées
    
    # Si l'opération est une modification
    elif operation == "edit":
        entrees_tableau.item(iid, values=(nom, numero, email, favori)) # Modifier les informations de l'entrée dans le tableau des entrées

    # Pour prévenir de changement non-enregistré
    global changements_effectues
    changements_effectues = True


def ouvrir_fenetre_ajouter()->None:
    '''
    Fenêtre pour ajouter une entrée au répertoire (nom, numéro, e-mail, favori/non-favori) (s'ouvre uniquement si répertoire ouvert)

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Si résultats d'une recherche affichés
    if est_dans_recherche:
        message_popup("Erreur", "src/error.gif", 'Ajout impossible dans résultats de recherche, veuillez réinitialiser la recherche!', "src/win_xp_error.mp3")
        return

    # Vérifier qu'un répertoire est ouvert
    if not repertoire_ouvert_verif(): return

    # Caractéristiques de la fenêtre
    fenetre_ajouter = Toplevel(fenetre_principale) # Fenêtre au-dessus de la fenêtre principale
    fenetre_ajouter.title("Ajouter") # Titre de la fenêtre
    fenetre_ajouter.resizable(0, 0)  # Taille non-modifiable

    # Textes à côté des champs de saisie
    nom_texte = Label(fenetre_ajouter, text="Nom :")
    numero_texte = Label(fenetre_ajouter, text="Numéro :")
    email_texte = Label(fenetre_ajouter, text="E-mail :")
    favori_texte = Label(fenetre_ajouter, text="Favori ?")

    # Placer les textes en colonne tout à gauche
    nom_texte.grid(row=0, column=0, padx=5)
    numero_texte.grid(row=1, column=0, padx=5)
    email_texte.grid(row=2, column=0, padx=5)
    favori_texte.grid(row=3, column=0, padx=5)

    # Champs de saisie
    nom_champ_de_saisie = Entry(fenetre_ajouter)
    numero_champ_de_saisie = Entry(fenetre_ajouter)
    email_champ_de_saisie = Entry(fenetre_ajouter)

    # Case à cocher pour favori
    est_favori = StringVar()
    favori_case_a_cocher = Checkbutton(fenetre_ajouter, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite
    nom_champ_de_saisie.grid(row=0, column=1, padx=5, pady=5)
    numero_champ_de_saisie.grid(row=1, column=1, padx=5, pady=(0,5))
    email_champ_de_saisie.grid(row=2, column=1, padx=5, pady=(0,5))
    favori_case_a_cocher.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    # Bouton d'ajout
    ajout_bouton = Button(fenetre_ajouter, text="Ajouter", command=lambda: ajouter_ou_modifier_et_inserer('add', None, nom_champ_de_saisie.get(), numero_champ_de_saisie.get(), email_champ_de_saisie.get(), est_favori.get()))
    ajout_bouton.grid(row=4, column=0, columnspan=2, padx=5, pady=5) # Placer le bouton en bas au centre de la fenêtre


def supprimer_entree()->None:
    '''
    Supprimer l'entrée sélectionnée du répertoire et l'effacer du tableau des entrées

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Vérifier qu'un répertoire est ouvert
    if not repertoire_ouvert_verif(): return

    # Obtenir l'identifiant et le nom de l'entrée sélectionnée
    entree = entree_selectionnee()
    iid = entree[0]
    name = entree[1]

    # Si aucune entrée n'a été cliquée
    if not name:
        message_popup("Erreur", "src/error.gif", "Aucune entrée n'est sélectionnée!", ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas supprimer

    # Supprimer l'entrée
    rep.rem_rep(repertoire, str(name)) # Supprimer l'entrée du répertoire
    entrees_tableau.delete(iid) # Supprimer l'entrée du tableau

    # Pour prévenir de changement non-enregistré
    global changements_effectues
    changements_effectues = True


def ouvrir_fenetre_modifier():
    '''
    Fenêtre pour modifier une entrée au répertoire (numéro, e-mail, favori/non-favori) (s'ouvre uniquement si répertoire ouvert)

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Vérifie qu'un répertoire est ouvert
    if not repertoire_ouvert_verif(): return

    # Obtenir l'identifiant et le nom de l'entrée sélectionnée
    entree = entree_selectionnee()
    iid = entree[0]
    name = entree[1]

    # Si aucune entrée n'est sélectionnée
    if not name:
        message_popup("Erreur", "src/error.gif", "Aucune entrée n'est sélectionnée!", ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas affiche la fenêtre de modification

    # Caractéristiques de la fenêtre
    fenetre_modifier = Toplevel(fenetre_principale)  # Fenêtre au-dessus de la fenêtre principale
    fenetre_modifier.title("Modifier") # Titre de la fenêtre
    fenetre_modifier.resizable(0, 0)   # Taille non-modifiable

    # Texte à côté des champs de saisie
    nom_texte = Label(fenetre_modifier, text="Nom :")
    numero_texte = Label(fenetre_modifier, text="Numéro :")
    email_texte = Label(fenetre_modifier, text="E-mail :")
    favori_texte = Label(fenetre_modifier, text="Favori ?")

    # Placer les textes en colonne tout à gauche
    nom_texte.grid(row=0, column=0, padx=5)
    numero_texte.grid(row=1, column=0, padx=5)
    email_texte.grid(row=2, column=0, padx=5)
    favori_texte.grid(row=3, column=0, padx=5)

    # Récuperer les informations de l'entrée
    name = str(name)
    number = repertoire[name][0]
    email = repertoire[name][1]
    est_favori = StringVar()
    est_favori.set(repertoire[name][2])

    # Champs de saisie
    nom_champ_de_saisie = Entry(fenetre_modifier)
    numero_champ_de_saisie = Entry(fenetre_modifier)
    email_champ_de_saisie = Entry(fenetre_modifier)

    # Insérer les informations de l'entrée dans les champs de saisie
    nom_champ_de_saisie.insert(END, name)
    nom_champ_de_saisie.config(state=DISABLED) # Empêcher la modification du nom
    numero_champ_de_saisie.insert(END, number)
    email_champ_de_saisie.insert(END, email)

    # Case à cocher pour favori et cocher/décocher si favori/non-favori
    favori_case_a_cocher = Checkbutton(fenetre_modifier, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite
    nom_champ_de_saisie.grid(row=0, column=1, padx=5, pady=5)
    numero_champ_de_saisie.grid(row=1, column=1, padx=5, pady=(0,5))
    email_champ_de_saisie.grid(row=2, column=1, padx=5, pady=(0,5))
    favori_case_a_cocher.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    # Bouton de modification
    ajout_bouton = Button(fenetre_modifier, text="Enregistrer", command=lambda: ajouter_ou_modifier_et_inserer('edit', iid, nom_champ_de_saisie.get(), numero_champ_de_saisie.get(), email_champ_de_saisie.get(), est_favori.get()))
    ajout_bouton.grid(row=4, column=0, columnspan=2, padx=5, pady=5) # Placer le bouton en bas au centre de la fenêtre


def reinitialiser_recherche()->None:
    '''
    Réinitialiser les résultats d'une recherche

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Réinitialiser le tableau d'entrées et placer toutes les entrées du répertoire
    effacer_tableau_et_inserer(repertoire)

    # Réactiver ajout d'entrée
    global est_dans_recherche
    est_dans_recherche = False


def rechercher_et_inserer(critere:str, nom:str, numero:str, email:str, est_favori:bool)->None:
    '''
    Rechercher selon le nom/numero/email/favori et affiche les résultats dans le tableau des entrées

    Paramètres :
    - critere (str) : "nom" ou "numero" ou "email" ou "favori"
    - nom (str) : Nom
    - numero (str) : Numéro
    - email (str) : E-mail
    - est_favori (bool) : Favori/non-favori (True/False)

    Renvoie :
    None
    '''

    # Si aucun critère n'est sélectionné
    if not critere:
        message_popup("Erreur", "src/error.gif", "Aucun critère n'est sélectionné!", ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas effectuer de recherche

    # Rechercher en fonction du critère sélectionné
    if critere == "nom":
        resultat_recherche = rep.search_name(repertoire, nom) # Rechercher en fonction du nom
    elif critere == "numero":
        resultat_recherche = rep.search_number(repertoire, numero) # Rechercher en fonction du numéro
    elif critere == "email":
        resultat_recherche = rep.search_email(repertoire, email) # Rechercher en fonction de l'e-mail
    elif critere == "favori":
        resultat_recherche = rep.search_favorite(repertoire, est_favori) # Rechercher en fonction du favori/non-favori

    # Afficher les résultats de la recherche dans le tableau d'entrées
    effacer_tableau_et_inserer(resultat_recherche)

    # Désactiver l'ajout d'entrée
    global est_dans_recherche
    est_dans_recherche = True


def ouvrir_fenetre_rechercher()->None:
    '''
    Fenêtre de recherche (s'ouvre uniquement si répertoire ouvert)

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Vérifie qu'un répertoire est ouvert
    if not repertoire_ouvert_verif(): return

    # Caractéristiques de la fenêtre
    fenetre_rechercher = Toplevel(fenetre_principale)
    fenetre_rechercher.title("Rechercher")
    fenetre_rechercher.resizable(0, 0)

    # Bouton radio pour sélectionner le critère de recherche
    critere_recherche = StringVar()
    nom_bouton_radio = Radiobutton(fenetre_rechercher, variable=critere_recherche, value="nom")
    numero_bouton_radio = Radiobutton(fenetre_rechercher, variable=critere_recherche, value="numero")
    email_bouton_radio = Radiobutton(fenetre_rechercher, variable=critere_recherche, value="email")
    favori_bouton_radio = Radiobutton(fenetre_rechercher, variable=critere_recherche, value="favori")

    # Placer les boutons radio tout à gauche sur la même colonne
    nom_bouton_radio.grid(row=0, column=0, padx=5)
    numero_bouton_radio.grid(row=1, column=0, padx=5)
    email_bouton_radio.grid(row=2, column=0, padx=5)
    favori_bouton_radio.grid(row=3, column=0, padx=5)

    # Texte à côté des champs de saisie
    nom_texte = Label(fenetre_rechercher, text="Nom :")
    numero_texte = Label(fenetre_rechercher, text="Numéro :")
    email_texte = Label(fenetre_rechercher, text="E-mail :")
    favori_texte = Label(fenetre_rechercher, text="Favori ?")

    # Placer les textes entres les boutons radios et les champs de saisie
    nom_texte.grid(row=0, column=1, padx=(0,5))
    numero_texte.grid(row=1, column=1, padx=(0,5))
    email_texte.grid(row=2, column=1, padx=(0,5))
    favori_texte.grid(row=3, column=1, padx=(0,5))

    # Champs de saisie
    nom_champ_de_saisie = Entry(fenetre_rechercher)
    numero_champ_de_saisie = Entry(fenetre_rechercher)
    email_champ_de_saisie = Entry(fenetre_rechercher)

    # Case à cocher pour favori
    est_favori = StringVar()
    favori_case_a_cocher = Checkbutton(fenetre_rechercher, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite    
    nom_champ_de_saisie.grid(row=0, column=2, padx=5, pady=5)
    numero_champ_de_saisie.grid(row=1, column=2, padx=5, pady=(0,5))
    email_champ_de_saisie.grid(row=2, column=2, padx=5, pady=(0,5))
    favori_case_a_cocher.grid(row=3, column=2, padx=5, pady=(0,5), sticky='w')

    # Cadre pour les boutons standards
    bouton_cadre = Frame(fenetre_rechercher) 
    bouton_cadre.grid(row=4, column=0, columnspan=3, padx=5, pady=5) # Placer le cadre en bas

    # Boutons de recherche et de réinitialisation de recherche
    rechercher_bouton = Button(bouton_cadre, text="Rechercher", command=lambda: rechercher_et_inserer(critere_recherche.get(), nom_champ_de_saisie.get(), numero_champ_de_saisie.get(), email_champ_de_saisie.get(), bool(est_favori.get())))
    reinitialiser_bouton = Button(bouton_cadre, text="Réinitialiser", command=reinitialiser_recherche)

    # Placer les boutons sur la même ligne dans le cadre et centre les boutons
    rechercher_bouton.grid(row=0, column=0, padx=5)
    reinitialiser_bouton.grid(row=0, column=1, padx=5)


def ouvrir_fenetre_aide()->None:
    '''
    Fenêtre d'aide avec une explication pour chaque bouton d'action

    Paramètres :
    Aucun

    Renvoie :
    None
    '''
    
    # Caractéristiques de la fenêtre
    fenetre_aide = Toplevel(fenetre_principale) # Fenêtre au-dessus de la fenêtre principale
    fenetre_aide.title("Aide")    # Titre de la fenêtre
    fenetre_aide.resizable(0,0)   # Taille non-modifiable

    # Fonction anonyme pour changer le texte d'explication
    changer_texte_explication = lambda text: explication_texte.config(text=text)

    # Boutons d'actions à cliquer pour changer d'explication
    nouveau_repertoire_bouton = Button(fenetre_aide, image=nouveau_repertoire_image, borderwidth=0, command=lambda: changer_texte_explication(nouveau_repertoire_explication))
    ouvrir_repertoire_bouton = Button(fenetre_aide, image=ouvrir_repertoire_image, borderwidth=0, command=lambda: changer_texte_explication(ouvrir_repertoire_explication))
    enregistrer_bouton = Button(fenetre_aide, image=enregistrer_image, borderwidth=0, command=lambda: changer_texte_explication(enregistrer_explication))
    ajouter_bouton = Button(fenetre_aide, image=ajouter_image, borderwidth=0, command=lambda: changer_texte_explication(ajouter_explication))
    supprimer_bouton = Button(fenetre_aide, image=supprimer_image, borderwidth=0, command=lambda: changer_texte_explication(supprimer_explication))
    modifier_bouton = Button(fenetre_aide, image=modifier_image, borderwidth=0, command=lambda: changer_texte_explication(modifier_explication))
    rechercher_bouton = Button(fenetre_aide, image=rechercher_image, borderwidth=0, command=lambda: changer_texte_explication(rechercher_explication))
    aide_bouton = Button(fenetre_aide, image=aide_image, borderwidth=0, command=lambda: changer_texte_explication(aide_explication))

    # Placer les boutons d'actions sur la même ligne en haut
    nouveau_repertoire_bouton.grid(row=0, column=0, padx=8, pady=8)
    ouvrir_repertoire_bouton.grid(row=0, column=1, padx=8)
    enregistrer_bouton.grid(row=0, column=2, padx=8)
    ajouter_bouton.grid(row=0, column=3, padx=8)
    supprimer_bouton.grid(row=0, column=4, padx=8)
    modifier_bouton.grid(row=0, column=5, padx=8)
    rechercher_bouton.grid(row=0, column=6, padx=8)
    aide_bouton.grid(row=0, column=7, padx=8)

    # Texte d'explication
    explication_texte = Label(fenetre_aide, text="Cliquez sur une des icônes pour obtenir une explication")
    explication_texte.grid(row=1, columnspan=8, pady=(0,8)) # Placer le texte au centre en bas

    # Explications pour chaque bouton d'action
    nouveau_repertoire_explication = "Créer un nouveau répertoire dans un fichier au format CSV"
    ouvrir_repertoire_explication = "Ouvrir un répertoire à partir d'un fichier au format CSV"
    enregistrer_explication = "Enregistrer les modifications faites au répertoire"
    ajouter_explication = "Ajouter une entrée au répertoire"
    supprimer_explication = "Supprimer une entrée du répertoire"
    modifier_explication = "Modifier une entrée du répertoire"
    rechercher_explication = "Chercher des entrées à partir du nom/numéro/e-mail/favoris"
    aide_explication = "Ouvrir cette fenêtre"


# Fenêtre principale
fenetre_principale = Tk() # Initialiser la fenêtre
fenetre_principale.wm_title("Repyrtoire") # Titre de la fenêtre
fenetre_principale.resizable(0, 0) # Taille non-modifiable

# Images pour les boutons d'actions (réutilisées dans la fenêtre d'aide)
nouveau_repertoire_image = PhotoImage(file="src/new.png")
ouvrir_repertoire_image = PhotoImage(file="src/open.png")
enregistrer_image = PhotoImage(file="src/save.png")
ajouter_image = PhotoImage(file="src/add.png")
supprimer_image = PhotoImage(file="src/remove.png")
modifier_image = PhotoImage(file="src/edit.png")
rechercher_image = PhotoImage(file="src/search.png")
aide_image = PhotoImage(file="src/help.png")

# Boutons d'actions
nouveau_repertoire_bouton = Button(fenetre_principale, image=nouveau_repertoire_image, command=nouveau_repertoire, borderwidth=0)
ouvrir_repertoire_bouton = Button(fenetre_principale, image=ouvrir_repertoire_image, command=ouvrir_repertoire, borderwidth=0)
enregistrer_bouton = Button(fenetre_principale, image=enregistrer_image, command=enregistrer, borderwidth=0)
ajouter_bouton = Button(fenetre_principale, image=ajouter_image, command=ouvrir_fenetre_ajouter, borderwidth=0)
supprimer_bouton = Button(fenetre_principale, image=supprimer_image, command=supprimer_entree, borderwidth=0)
modifier_bouton = Button(fenetre_principale, image=modifier_image, command=ouvrir_fenetre_modifier, borderwidth=0)
rechercher_bouton = Button(fenetre_principale, image=rechercher_image, command=ouvrir_fenetre_rechercher, borderwidth=0)
aide_bouton = Button(fenetre_principale, image=aide_image, command=ouvrir_fenetre_aide, borderwidth=0)

# Placer les boutons d'actions sur la même ligne en haut
nouveau_repertoire_bouton.grid(row=0, column=0, padx=8, pady=8)
ouvrir_repertoire_bouton.grid(row=0, column=1, padx=8)
enregistrer_bouton.grid(row=0, column=2, padx=8)
ajouter_bouton.grid(row=0, column=3, padx=8)
supprimer_bouton.grid(row=0, column=4, padx=8)
modifier_bouton.grid(row=0, column=5, padx=8)
rechercher_bouton.grid(row=0, column=6, padx=8)
aide_bouton.grid(row=0, column=7, padx=8)

# Cadre pour le tableau d'entrées et sa barre de défilement
entrees_cadre = Frame(fenetre_principale)
entrees_cadre.grid(row=1, column=0, columnspan=8) # Placer le cadre en bas en prenant la même longueur que la totalité des boutons d'actions

# Tableau d'entrées
entrees_tableau = ttk.Treeview(entrees_cadre, selectmode='browse')
entrees_tableau['columns'] = ('nom', 'numero', 'email', 'favori')

# Colonnes du tableau
entrees_tableau.column("#0", width=0,  stretch=NO)
entrees_tableau.column("nom",anchor=CENTER, width=80)
entrees_tableau.column("numero",anchor=CENTER,width=100)
entrees_tableau.column("email",anchor=CENTER,width=220)
entrees_tableau.column("favori",anchor=CENTER,width=30)

# En-têtes du tableau (textes placés au centre)
entrees_tableau.heading("#0",text="",anchor=CENTER)
entrees_tableau.heading("nom",text="Nom",anchor=CENTER)
entrees_tableau.heading("numero",text="Numéro",anchor=CENTER)
entrees_tableau.heading("email",text="E-mail",anchor=CENTER)
entrees_tableau.heading("favori",text="★",anchor=CENTER)

# Sélectionner une entrée avec le clic gauche de la souris
entrees_tableau.bind('<ButtonRelease-1>', entree_selectionnee)

# Placer le tableau à gauche et prendre la quasi-totalité de la place disponible (place restante pour la barre de défilement)
entrees_tableau.pack(side=LEFT, fill=BOTH, expand=True)

# Barre de défilement pour le tableau d'entrées
entrees_scrollbar = Scrollbar(entrees_cadre, orient=VERTICAL, command=entrees_tableau.yview) # Barre de défilement verticale
entrees_tableau.configure(yscrollcommand=entrees_scrollbar.set) # Lier la barre de défilement au tableau d'entrées
entrees_scrollbar.pack(side=RIGHT, fill=Y) # Placer la barre de défilement à droite du cadre et prendre toute la place

# Boucle principale
fenetre_principale.mainloop()
