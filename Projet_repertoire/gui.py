from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer # Pour le son
import repertoire_nolan_merwan as rep

global repertoire
global repertoire_ouvert
repertoire_ouvert = False

# Easter egg
mixer.init()
sound_file_path = 'src/win_xp_error.mp3'
mixer.music.load(sound_file_path)

# Fenêtre d'erreur
def message_erreur(erreur):
    message_erreur_window = Toplevel(root.winfo_toplevel())
    message_erreur_window.title("Erreur")
    message_erreur_window.resizable(0, 0)
    message_erreur_window.grab_set()
    mixer.music.play()

    erreur_image = PhotoImage(file="src/error.gif")
    erreur_image_button = Button(message_erreur_window, image=erreur_image, command=lambda: mixer.music.play(), borderwidth=0)
    erreur_image_button.image = erreur_image

    erreur_image_button.grid(row=0, column=0, padx=(5, 0), pady=5)
    erreur_label = Label(message_erreur_window, text=erreur)
    erreur_label.grid(row=0, column=1, padx=(0,5), pady=5)

# Obtenir l'entrée qui a été sélectionnée
def entree_selectionnee(*_):
    try:
        iid = entrees_table.focus()
        name = entrees_table.item(iid)['values'][0]
    except IndexError:
        name = None
    finally:
        return iid, name

# Supprimer une entrée du répertoire
def remove():
    # Si le répertoire n'est pas ouvert
    if repertoire_ouvert == False:
        message_erreur("Le répertoire n'est pas ouvert!")
        return

    entree = entree_selectionnee()
    iid = entree[0]
    name = entree[1]

    # Si aucune entrée n'a été cliquée
    if not name:
        message_erreur("Aucune entrée n'est sélectionnée!")
        return

    rep.rem_rep(repertoire, name)
    entrees_table.delete(iid)

# Ouvrir le répertoire
def open_file():
    global repertoire, filename
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filename: return # Si la boîte de dialogue a été fermée sans ouvrir de fichier

    repertoire = rep.init_rep(filename)
    clear_table()
    for name in repertoire.keys():
        number = repertoire[name][0]
        email = repertoire[name][1]
        favorite = repertoire[name][2]
        entrees_table.insert(parent='',index='end', text='', values=(name, number, email, favorite))

    global repertoire_ouvert
    repertoire_ouvert = True

# Réinitialise le tableau d'entrées
def clear_table():
   for entree in entrees_table.get_children():
      entrees_table.delete(entree)

# Ajouter l'élement au répertoire et l'affiche
def add_or_edit_and_insert(operation, iid, nom, numero, email, est_favori):
    # Si l'entrée existe déjà dans le répertoire
    if nom in repertoire and operation == 'add':
        message_erreur('Une entrée associée à ce nom existe déjà!'); return
    # Si le nom est vide
    if not nom:
        message_erreur('Le nom ne peut pas être vide!'); return
    # Si ni le numéro ni l'email n'a été donné
    if not(numero or email):
        message_erreur('Pas de numéro/email!'); return
    # Si le numéro contient autre chose que des chiffres
    numero = numero.strip()
    if not numero.isdigit():
        message_erreur('Numéro invalide!'); return

    rep.add_edit_rep(repertoire, nom, numero, email, est_favori)
    if operation == 'add':
        entrees_table.insert(parent='',index='end', text='', values=(nom, numero, email, est_favori))
    elif operation == 'edit':
        entrees_table.item(iid, values=(nom, numero, email, est_favori))


# Ajouter une entrée au répertoire
def add_dialog():
    if repertoire_ouvert == False:
        message_erreur("Le répertoire n'est pas ouvert!")
        return

    add_dialog_window = Toplevel(root)
    add_dialog_window.title("Ajouter")
    add_dialog_window.resizable(0, 0)

    name_label = Label(add_dialog_window, text="Nom :")
    number_label = Label(add_dialog_window, text="Numéro :")
    email_label = Label(add_dialog_window, text="E-mail :")
    favorite_label = Label(add_dialog_window, text="Favori ?")

    name_label.grid(row=0, column=0, padx=5)
    number_label.grid(row=1, column=0, padx=5)
    email_label.grid(row=2, column=0, padx=5)
    favorite_label.grid(row=3, column=0, padx=5)

    name_entry = Entry(add_dialog_window)
    number_entry = Entry(add_dialog_window)
    email_entry = Entry(add_dialog_window)

    est_favori = StringVar()
    favorite_checkbox = Checkbutton(add_dialog_window, variable=est_favori, onvalue='★', offvalue='')

    name_entry.grid(row=0, column=1, padx=5, pady=5)
    number_entry.grid(row=1, column=1, padx=5, pady=(0,5))
    email_entry.grid(row=2, column=1, padx=5, pady=(0,5))
    favorite_checkbox.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    confirm_button = Button(add_dialog_window, text="Ajouter", command=lambda: add_or_edit_and_insert('add', name_entry.get(), number_entry.get(), email_entry.get(), est_favori.get()))
    confirm_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Modifier une entrée du répertoire
def edit_dialog():
    if repertoire_ouvert == False:
        message_erreur("Le répertoire n'est pas ouvert!")
        return

    edit_dialog_window = Toplevel(root)
    edit_dialog_window.title("Modifier")
    edit_dialog_window.resizable(0, 0)

    name_label = Label(edit_dialog_window, text="Nom :")
    number_label = Label(edit_dialog_window, text="Numéro :")
    email_label = Label(edit_dialog_window, text="E-mail :")
    favorite_label = Label(edit_dialog_window, text="Favori ?")

    name_label.grid(row=0, column=0, padx=5)
    number_label.grid(row=1, column=0, padx=5)
    email_label.grid(row=2, column=0, padx=5)
    favorite_label.grid(row=3, column=0, padx=5)

    iid = entree_selectionnee()[0]
    name = entree_selectionnee()[1]
    number = repertoire[name][0]
    email = repertoire[name][1]
    est_favori = StringVar()
    est_favori.set(repertoire[name][2])

    name_entry = Entry(edit_dialog_window)
    name_entry.insert(END, name)
    name_entry.config(state=DISABLED)
    number_entry = Entry(edit_dialog_window)
    number_entry.insert(END, number)
    email_entry = Entry(edit_dialog_window)
    email_entry.insert(END, email)

    favorite_checkbox = Checkbutton(edit_dialog_window, variable=est_favori, onvalue='★', offvalue='')

    name_entry.grid(row=0, column=1, padx=5, pady=5)
    number_entry.grid(row=1, column=1, padx=5, pady=(0,5))
    email_entry.grid(row=2, column=1, padx=5, pady=(0,5))
    favorite_checkbox.grid(row=3, column=1, padx=5, pady=(0,5), sticky='w')

    confirm_button = Button(edit_dialog_window, text="Enregistrer", command=lambda: add_or_edit_and_insert('edit', iid, name_entry.get(), number_entry.get(), email_entry.get(), est_favori.get()))
    confirm_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)    


# Fenêtre

root = Tk()
root.wm_title("Repyrtoire")
root.resizable(0, 0)

# Boutons

new_image = PhotoImage(file="src/new.png")
new_button = Button(root, image=new_image, command=open, borderwidth=0)
new_button.grid(row=0, column=0, padx=(14,8), pady=8)

open_image = PhotoImage(file="src/open.png")
open_button = Button(root, image=open_image, command=open_file, borderwidth=0)
open_button.grid(row=0, column=1, padx=8)

save_image = PhotoImage(file="src/save.png")
save_button = Button(root, image=save_image, command=open, borderwidth=0)
save_button.grid(row=0, column=2, padx=8)

add_image = PhotoImage(file="src/add.png")
add_button = Button(root, image=add_image, command=add_dialog, borderwidth=0)
add_button.grid(row=0, column=3, padx=8)

remove_image = PhotoImage(file="src/remove.png")
remove_button = Button(root, image=remove_image, command=remove, borderwidth=0)
remove_button.grid(row=0, column=4, padx=8)

edit_image = PhotoImage(file="src/edit.png")
edit_button = Button(root, image=edit_image, command=edit_dialog, borderwidth=0)
edit_button.grid(row=0, column=5, padx=8)

search_image = PhotoImage(file="src/search.png")
search_button = Button(root, image=search_image, command=open, borderwidth=0)
search_button.grid(row=0, column=6, padx=8)

help_image = PhotoImage(file="src/help.png")
help_button = Button(root, image=help_image, command=open, borderwidth=0)
help_button.grid(row=0, column=7, padx=8)

# Tableau des entrées

entrees_frame = Frame(root)
entrees_frame.grid(row=1, column=0, columnspan=8)

entrees_table = ttk.Treeview(entrees_frame, selectmode='browse')
entrees_table['columns'] = ('nom', 'numero', 'email', 'favori')

entrees_table.column("#0", width=0,  stretch=NO)
entrees_table.column("nom",anchor=CENTER, width=80)
entrees_table.column("numero",anchor=CENTER,width=100)
entrees_table.column("email",anchor=CENTER,width=220)
entrees_table.column("favori",anchor=CENTER,width=30)

entrees_table.heading("#0",text="",anchor=CENTER)
entrees_table.heading("nom",text="Nom",anchor=CENTER)
entrees_table.heading("numero",text="Numéro",anchor=CENTER)
entrees_table.heading("email",text="E-mail",anchor=CENTER)
entrees_table.heading("favori",text="★",anchor=CENTER)

entrees_table.bind('<ButtonRelease-1>', entree_selectionnee)

entrees_table.pack(side=LEFT, fill=BOTH, expand=True)

# Barre de défilement

entrees_scrollbar = Scrollbar(entrees_frame, orient=VERTICAL, command=entrees_table.yview)
entrees_table.configure(yscrollcommand=entrees_scrollbar.set)
entrees_scrollbar.pack(side=RIGHT, fill=Y)



root.mainloop()