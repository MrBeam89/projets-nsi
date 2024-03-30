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
    message_popup_window = Toplevel(root.winfo_toplevel()) # Toujours au-dessus de la fenêtre le plus au-dessus
    message_popup_window.title(titre) # Titre de la fenêtre
    message_popup_window.resizable(0, 0) # Taille non-modifiable
    message_popup_window.grab_set() # Rendre impossible interaction avec les autres fenêtres tant que celle-ci n'est pas fermée

    # Jouer un son
    mixer.music.load(sound_file_path) # Charger le son
    mixer.music.play() # Jouer le son

    # Image
    popup_image = PhotoImage(file=image_file_path) # Ouvrir l'image à partir du chemin d'accès au fichier
    popup_image_button = Button(message_popup_window, image=popup_image, command=lambda: mixer.music.play(), borderwidth=0) # Bouton-image qui joue le son lorsqu'il est cliqué
    popup_image_button.image = popup_image # Pour éviter que le ramasse-miettes de Python supprime l'image
    popup_image_button.grid(row=0, column=0, padx=(5, 0), pady=5) # Placer l'image à gauche du message sur la même ligne

    # Message
    popup_label = Label(message_popup_window, text=message) # Message donné en paramètre
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
        iid = entrees_table.focus() # Obtenir l'identifiant de l'entrée sélectionnée dans le tableau
        name = entrees_table.item(iid)['values'][0] # Obtenir le nom de l'entrée
    except IndexError: # Si l'en-tête du tableau est cliqué
        name = None
    finally:
        return iid, name # Renvoyer l'identifiant et le nom


def clear_table_and_insert(dic:dict)->None:
    '''
    Effacer tous les élements du tableau et insérer tous ceux dans le dictionnaire donné

    Paramètres :
    - dic (dict) : Répertoire ou résultats d'une recherche

    Renvoie :
    None
    '''

    # Supprimer toutes les entrées à l'écran
    for entree in entrees_table.get_children():
      entrees_table.delete(entree)

    # Rajouter toutes les entrées dans le dictionnaire donné
    for nom, valeur in dic.items(): # Pour chaque entrée dans le dictionnaire
        numero = valeur[0]
        email = valeur[1]
        favori = valeur[2]
        entrees_table.insert(parent='', index='end', text='', values=(nom, numero, email, favori)) # Insérer l'entrée dans le tableau des entrées


def new_file()->None:
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
    clear_table_and_insert(repertoire)

    # Activer les fonctions de modification/recherche
    repertoire_ouvert = True
    changements_effectues = False


def open_file()->None:
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
    clear_table_and_insert(repertoire)

    # Activer les fonctions de modification/recherche
    repertoire_ouvert = True
    changements_effectues = False


def save()->None:
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


def add_or_edit_and_insert(operation:str, iid:int, nom:str, numero:str, email:str, favori:str)->None:
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

    # Si le numéro contient autre chose que des chiffres
    numero = numero.strip() # Enlever les espaces au début et à la fin
    if not numero.isdigit():
        message_popup("Erreur", "src/error.gif", 'Numéro invalide!', ERROR_SFX_FILEPATH) # Afficher un message d'erreur via une fenêtre popup
        return # Ne pas ajouter/modifier

    # Ajouter/modifier l'entrée dans le répertoire si aucune erreur n'est détectée
    rep.add_edit_rep(repertoire, nom, numero, email, favori)

    # Si l'opération est un ajout
    if operation == "add":
        entrees_table.insert(parent='',index='end', text='', values=(nom, numero, email, favori)) # Ajouter l'entrée dans le tableau des entrées
    
    # Si l'opération est une modification
    elif operation == "edit":
        entrees_table.item(iid, values=(nom, numero, email, favori)) # Modifier les informations de l'entrée dans le tableau des entrées

    # Pour prévenir de changement non-enregistré
    global changements_effectues
    changements_effectues = True


def add_dialog()->None:
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
    add_dialog_window = Toplevel(root) # Fenêtre au-dessus de la fenêtre principale
    add_dialog_window.title("Ajouter") # Titre de la fenêtre
    add_dialog_window.resizable(0, 0)  # Taille non-modifiable

    # Textes à côté des champs de saisie
    name_label = Label(add_dialog_window, text="Nom :")
    number_label = Label(add_dialog_window, text="Numéro :")
    email_label = Label(add_dialog_window, text="E-mail :")
    favorite_label = Label(add_dialog_window, text="Favori ?")

    # Placer les textes en colonne tout à gauche
    name_label.grid(row=0, column=0, padx=5)
    number_label.grid(row=1, column=0, padx=5)
    email_label.grid(row=2, column=0, padx=5)
    favorite_label.grid(row=3, column=0, padx=5)

    # Champs de saisie
    name_entry = Entry(add_dialog_window)
    number_entry = Entry(add_dialog_window)
    email_entry = Entry(add_dialog_window)

    # Case à cocher pour favori
    est_favori = StringVar()
    favorite_checkbox = Checkbutton(add_dialog_window, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    number_entry.grid(row=1, column=1, padx=5, pady=(0,5))
    email_entry.grid(row=2, column=1, padx=5, pady=(0,5))
    favorite_checkbox.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    # Bouton d'ajout
    confirm_button = Button(add_dialog_window, text="Ajouter", command=lambda: add_or_edit_and_insert('add', None, name_entry.get(), number_entry.get(), email_entry.get(), est_favori.get()))
    confirm_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5) # Placer le bouton en bas au centre de la fenêtre


def remove()->None:
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
    entrees_table.delete(iid) # Supprimer l'entrée du tableau

    # Pour prévenir de changement non-enregistré
    global changements_effectues
    changements_effectues = True


def edit_dialog():
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
    edit_dialog_window = Toplevel(root)  # Fenêtre au-dessus de la fenêtre principale
    edit_dialog_window.title("Modifier") # Titre de la fenêtre
    edit_dialog_window.resizable(0, 0)   # Taille non-modifiable

    # Texte à côté des champs de saisie
    name_label = Label(edit_dialog_window, text="Nom :")
    number_label = Label(edit_dialog_window, text="Numéro :")
    email_label = Label(edit_dialog_window, text="E-mail :")
    favorite_label = Label(edit_dialog_window, text="Favori ?")

    # Placer les textes en colonne tout à gauche
    name_label.grid(row=0, column=0, padx=5)
    number_label.grid(row=1, column=0, padx=5)
    email_label.grid(row=2, column=0, padx=5)
    favorite_label.grid(row=3, column=0, padx=5)

    # Récuperer les informations de l'entrée
    name = str(name)
    number = repertoire[name][0]
    email = repertoire[name][1]
    est_favori = StringVar()
    est_favori.set(repertoire[name][2])

    # Champs de saisie
    name_entry = Entry(edit_dialog_window)
    number_entry = Entry(edit_dialog_window)
    email_entry = Entry(edit_dialog_window)

    # Insérer les informations de l'entrée dans les champs de saisie
    name_entry.insert(END, name)
    name_entry.config(state=DISABLED) # Empêcher la modification du nom
    number_entry.insert(END, number)
    email_entry.insert(END, email)

    # Case à cocher pour favori et cocher/décocher si favori/non-favori
    favorite_checkbox = Checkbutton(edit_dialog_window, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    number_entry.grid(row=1, column=1, padx=5, pady=(0,5))
    email_entry.grid(row=2, column=1, padx=5, pady=(0,5))
    favorite_checkbox.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    # Bouton de modification
    confirm_button = Button(edit_dialog_window, text="Enregistrer", command=lambda: add_or_edit_and_insert('edit', iid, name_entry.get(), number_entry.get(), email_entry.get(), est_favori.get()))
    confirm_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5) # Placer le bouton en bas au centre de la fenêtre


def reset_search()->None:
    '''
    Réinitialiser les résultats d'une recherche

    Paramètres :
    Aucun

    Renvoie :
    None
    '''

    # Réinitialiser le tableau d'entrées et placer toutes les entrées du répertoire
    clear_table_and_insert(repertoire)

    # Réactiver ajout d'entrée
    global est_dans_recherche
    est_dans_recherche = False


def search_and_insert(critere:str, nom:str, numero:str, email:str, est_favori:bool)->None:
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
    clear_table_and_insert(resultat_recherche)

    # Désactiver l'ajout d'entrée
    global est_dans_recherche
    est_dans_recherche = True


def search_dialog()->None:
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
    search_dialog_window = Toplevel(root)
    search_dialog_window.title("Rechercher")
    search_dialog_window.resizable(0, 0)

    # Bouton radio pour sélectionner le critère de recherche
    critere_recherche = StringVar()
    name_radiobutton = Radiobutton(search_dialog_window, variable=critere_recherche, value="nom")
    numero_radiobutton = Radiobutton(search_dialog_window, variable=critere_recherche, value="numero")
    email_radiobutton = Radiobutton(search_dialog_window, variable=critere_recherche, value="email")
    favori_radiobutton = Radiobutton(search_dialog_window, variable=critere_recherche, value="favori")

    # Placer les boutons radio tout à gauche sur la même colonne
    name_radiobutton.grid(row=0, column=0, padx=5)
    numero_radiobutton.grid(row=1, column=0, padx=5)
    email_radiobutton.grid(row=2, column=0, padx=5)
    favori_radiobutton.grid(row=3, column=0, padx=5)

    # Texte à côté des champs de saisie
    name_label = Label(search_dialog_window, text="Nom :")
    number_label = Label(search_dialog_window, text="Numéro :")
    email_label = Label(search_dialog_window, text="E-mail :")
    favorite_label = Label(search_dialog_window, text="Favori ?")

    # Placer les textes entres les boutons radios et les champs de saisie
    name_label.grid(row=0, column=1, padx=(0,5))
    number_label.grid(row=1, column=1, padx=(0,5))
    email_label.grid(row=2, column=1, padx=(0,5))
    favorite_label.grid(row=3, column=1, padx=(0,5))

    # Champs de saisie
    name_entry = Entry(search_dialog_window)
    number_entry = Entry(search_dialog_window)
    email_entry = Entry(search_dialog_window)

    # Case à cocher pour favori
    est_favori = StringVar()
    favorite_checkbox = Checkbutton(search_dialog_window, variable=est_favori, onvalue='★', offvalue='')

    # Placer les champs de saisie et la case à cocher dans la même colonne tout à droite    
    name_entry.grid(row=0, column=2, padx=5, pady=5)
    number_entry.grid(row=1, column=2, padx=5, pady=(0,5))
    email_entry.grid(row=2, column=2, padx=5, pady=(0,5))
    favorite_checkbox.grid(row=3, column=2, padx=5, pady=(0,5), sticky='w')

    # Cadre pour les boutons standards
    button_frame = Frame(search_dialog_window) 
    button_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5) # Placer le cadre en bas

    # Boutons de recherche et de réinitialisation de recherche
    search_button = Button(button_frame, text="Rechercher", command=lambda: search_and_insert(critere_recherche.get(), name_entry.get(), number_entry.get(), email_entry.get(), bool(est_favori.get())))
    reset_button = Button(button_frame, text="Réinitialiser", command=reset_search)

    # Placer les boutons sur la même ligne dans le cadre et centre les boutons
    search_button.grid(row=0, column=0, padx=5)
    reset_button.grid(row=0, column=1, padx=5)


def help_dialog()->None:
    '''
    Fenêtre d'aide avec une explication pour chaque bouton d'action

    Paramètres :
    Aucun

    Renvoie :
    None
    '''
    
    # Caractéristiques de la fenêtre
    help_dialog_window = Toplevel(root) # Fenêtre au-dessus de la fenêtre principale
    help_dialog_window.title("Aide")    # Titre de la fenêtre
    help_dialog_window.resizable(0,0)   # Taille non-modifiable

    # Fonction anonyme pour changer le texte d'explication
    change_explanation_text = lambda text: explanation_label.config(text=text)

    # Boutons d'actions à cliquer pour changer d'explication
    new_button = Button(help_dialog_window, image=new_image, borderwidth=0, command=lambda: change_explanation_text(new_text))
    open_button = Button(help_dialog_window, image=open_image, borderwidth=0, command=lambda: change_explanation_text(open_text))
    save_button = Button(help_dialog_window, image=save_image, borderwidth=0, command=lambda: change_explanation_text(save_text))
    add_button = Button(help_dialog_window, image=add_image, borderwidth=0, command=lambda: change_explanation_text(add_text))
    remove_button = Button(help_dialog_window, image=remove_image, borderwidth=0, command=lambda: change_explanation_text(remove_text))
    edit_button = Button(help_dialog_window, image=edit_image, borderwidth=0, command=lambda: change_explanation_text(edit_text))
    search_button = Button(help_dialog_window, image=search_image, borderwidth=0, command=lambda: change_explanation_text(search_text))
    help_button = Button(help_dialog_window, image=help_image, borderwidth=0, command=lambda: change_explanation_text(help_text))

    # Placer les boutons d'actions sur la même ligne en haut
    new_button.grid(row=0, column=0, padx=8, pady=8)
    open_button.grid(row=0, column=1, padx=8)
    save_button.grid(row=0, column=2, padx=8)
    add_button.grid(row=0, column=3, padx=8)
    remove_button.grid(row=0, column=4, padx=8)
    edit_button.grid(row=0, column=5, padx=8)
    search_button.grid(row=0, column=6, padx=8)
    help_button.grid(row=0, column=7, padx=8)

    # Texte d'explication
    explanation_label = Label(help_dialog_window, text="Cliquez sur une des icônes pour obtenir une explication")
    explanation_label.grid(row=1, columnspan=8, pady=(0,8)) # Placer le texte au centre en bas

    # Explications pour chaque bouton d'action
    new_text = "Créer un nouveau répertoire dans un fichier au format CSV"
    open_text = "Ouvrir un répertoire à partir d'un fichier au format CSV"
    save_text = "Enregistrer les modifications faites au répertoire"
    add_text = "Ajouter une entrée au répertoire"
    remove_text = "Supprimer une entrée du répertoire"
    edit_text = "Modifier une entrée du répertoire"
    search_text = "Chercher des entrées à partir du nom/numéro/e-mail/favoris"
    help_text = "Ouvrir cette fenêtre"


# Fenêtre principale
root = Tk() # Initialiser la fenêtre
root.wm_title("Repyrtoire") # Titre de la fenêtre
root.resizable(0, 0) # Taille non-modifiable

# Images pour les boutons d'actions (réutilisées dans la fenêtre d'aide)
new_image = PhotoImage(file="src/new.png")
open_image = PhotoImage(file="src/open.png")
save_image = PhotoImage(file="src/save.png")
add_image = PhotoImage(file="src/add.png")
remove_image = PhotoImage(file="src/remove.png")
edit_image = PhotoImage(file="src/edit.png")
search_image = PhotoImage(file="src/search.png")
help_image = PhotoImage(file="src/help.png")

# Boutons d'actions
new_button = Button(root, image=new_image, command=new_file, borderwidth=0)
open_button = Button(root, image=open_image, command=open_file, borderwidth=0)
save_button = Button(root, image=save_image, command=save, borderwidth=0)
add_button = Button(root, image=add_image, command=add_dialog, borderwidth=0)
remove_button = Button(root, image=remove_image, command=remove, borderwidth=0)
edit_button = Button(root, image=edit_image, command=edit_dialog, borderwidth=0)
search_button = Button(root, image=search_image, command=search_dialog, borderwidth=0)
help_button = Button(root, image=help_image, command=help_dialog, borderwidth=0)

# Placer les boutons d'actions sur la même ligne en haut
new_button.grid(row=0, column=0, padx=8, pady=8)
open_button.grid(row=0, column=1, padx=8)
save_button.grid(row=0, column=2, padx=8)
add_button.grid(row=0, column=3, padx=8)
remove_button.grid(row=0, column=4, padx=8)
edit_button.grid(row=0, column=5, padx=8)
search_button.grid(row=0, column=6, padx=8)
help_button.grid(row=0, column=7, padx=8)

# Cadre pour le tableau d'entrées et sa barre de défilement
entrees_frame = Frame(root)
entrees_frame.grid(row=1, column=0, columnspan=8) # Placer le cadre en bas en prenant la même longueur que la totalité des boutons d'actions

# Tableau d'entrées
entrees_table = ttk.Treeview(entrees_frame, selectmode='browse')
entrees_table['columns'] = ('nom', 'numero', 'email', 'favori')

# Colonnes du tableau
entrees_table.column("#0", width=0,  stretch=NO)
entrees_table.column("nom",anchor=CENTER, width=80)
entrees_table.column("numero",anchor=CENTER,width=100)
entrees_table.column("email",anchor=CENTER,width=220)
entrees_table.column("favori",anchor=CENTER,width=30)

# En-têtes du tableau
entrees_table.heading("#0",text="",anchor=CENTER)
entrees_table.heading("nom",text="Nom",anchor=CENTER)
entrees_table.heading("numero",text="Numéro",anchor=CENTER)
entrees_table.heading("email",text="E-mail",anchor=CENTER)
entrees_table.heading("favori",text="★",anchor=CENTER)

# Sélectionner une entrée avec le clic gauche de la souris
entrees_table.bind('<ButtonRelease-1>', entree_selectionnee)

# Placer le tableau à gauche et prendre la quasi-totalité de la place disponible (place restante pour la barre de défilement)
entrees_table.pack(side=LEFT, fill=BOTH, expand=True)

# Barre de défilement pour le tableau d'entrées
entrees_scrollbar = Scrollbar(entrees_frame, orient=VERTICAL, command=entrees_table.yview) # Barre de défilement verticale
entrees_table.configure(yscrollcommand=entrees_scrollbar.set) # Lier la barre de défilement au tableau d'entrées
entrees_scrollbar.pack(side=RIGHT, fill=Y) # Placer la barre de défilement à droite du cadre et prendre toute la place

# Boucle principale
root.mainloop()
