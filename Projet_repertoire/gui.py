from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import repertoire_nolan_merwan as rep

global repertoire

# Obtenir l'entrée qui a été sélectionnée
def entree_selectionnee(*_):
    try:
        iid = entrees_table.focus()
        print(entrees_table.item(iid))
        name = entrees_table.item(iid)['values'][0]
    except IndexError:
        name = None
    finally:
        return iid, name

# Supprimer une entrée du répertoire
def remove():
    entree = entree_selectionnee()
    iid = entree[0]
    name = entree[1]
    rep.rem_rep(repertoire, name)
    entrees_table.delete(iid)

# Ouvrir le répertoire
def open_file():
    global repertoire, filename
    filename = filedialog.askopenfilename()
    repertoire = rep.init_rep(filename)
    clear_table()
    for key in repertoire.keys():
        entrees_table.insert(parent='',index='end', text='', values=(key, repertoire[key], '', ''))

# Réinitialise le tableau d'entrées
def clear_table():
   for entree in entrees_table.get_children():
      entrees_table.delete(entree)

# Fenêtre

root = Tk()
root.wm_title("Repyrtoire")
root.resizable(0, 0)

# Boutons

open_image = PhotoImage(file="src/open.png")
open_button = Button(root, image=open_image, command=open_file, borderwidth=0)
open_button.grid(row=0, column=0, padx=(14,8), pady=8)

save_image = PhotoImage(file="src/save.png")
save_button = Button(root, image=save_image, command=open, borderwidth=0)
save_button.grid(row=0, column=1, padx=8)

add_image = PhotoImage(file="src/add.png")
add_button = Button(root, image=add_image, command=open, borderwidth=0)
add_button.grid(row=0, column=2, padx=8)

remove_image = PhotoImage(file="src/remove.png")
remove_button = Button(root, image=remove_image, command=remove, borderwidth=0)
remove_button.grid(row=0, column=3, padx=8)

edit_image = PhotoImage(file="src/edit.png")
edit_button = Button(root, image=edit_image, command=open, borderwidth=0)
edit_button.grid(row=0, column=4, padx=8)

favorite_image = PhotoImage(file="src/favorite.png")
favorite_button = Button(root, image=favorite_image, command=open, borderwidth=0)
favorite_button.grid(row=0, column=5, padx=8)

search_image = PhotoImage(file="src/search.png")
search_button = Button(root, image=search_image, command=open, borderwidth=0)
search_button.grid(row=0, column=6, padx=8)

help_image = PhotoImage(file="src/help.png")
help_button = Button(root, image=help_image, command=open, borderwidth=0)
help_button.grid(row=0, column=7, padx=8)

# Tableau des entrées

entrees_frame = Frame(root)
entrees_frame.grid(row=1, column=0, columnspan=8)

entrees_table = ttk.Treeview(entrees_frame)
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