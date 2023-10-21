# Numerical
# Conversion
# Interface
# Version GUI
# Par Nolan CACERES VASQUEZ et Merwan DE LA PENA TORTELLIER

from conversion import *
from tkinter import *
from tkinter import ttk # Pour la liste déroulante
from pygame import mixer # Pour le son

# Son d'explosion pour erreur
mixer.init()
sound_file_path = 'src/deltarune_explosion.wav'
mixer.music.load(sound_file_path)

# Créer le popup d'erreur
def summon_error_window():
        # Config de la fenêtre
        error_window = Toplevel()
        error_window.title("Erreur")
        error_window.geometry("200x60")
        error_window.resizable(0, 0)

        # Image de dynamite
        dynamite = PhotoImage(file='./src/bomb_dynamite.png')
        dynamite_label = Label(error_window, image=dynamite)
        dynamite_label.photo = dynamite

        error_label = Label(error_window, text="Nombre vide/invalide")

        # Placement des widgets
        dynamite_label.grid(row=0, column=1, padx=10, pady=10)
        error_label.grid(row=0, column=2, padx=10, pady=10)

        # B O O M
        mixer.music.play()


# Obtenir les nombres et les bases
def get_numbers_and_bases():
    bases = [first_menu.get(), second_menu.get()]
    numbers = [first_entry.get(), second_entry.get()]
    return [bases, numbers]

# Convertir de gauche à droite
def convert_first_to_second():
    numbers_and_bases = get_numbers_and_bases()
    number_to_convert = numbers_and_bases[1][0]

    # Vérifie si le nombre à convertir n'est pas vide et affiche la fenêtre d'erreur si oui
    if bool(number_to_convert.strip()) == False:
        summon_error_window()

    else:
        try:
            if numbers_and_bases[0][0] == "Décimal":
                number_to_convert = int(number_to_convert)
                if numbers_and_bases[0][1] == "Binaire":
                    converted_number = dec_to_bin(number_to_convert)
                if numbers_and_bases[0][1] == "Hexadécimal":
                   converted_number = dec_to_hexa(number_to_convert)

            if numbers_and_bases[0][0] == "Binaire":
                if numbers_and_bases[0][1] == "Décimal":
                    converted_number = bin_to_dec(number_to_convert)
                if numbers_and_bases[0][1] == "Hexadécimal":
                    converted_number = bin_to_hexa(number_to_convert)

            if numbers_and_bases[0][0] == "Hexadécimal":
                if numbers_and_bases[0][1] == "Décimal":
                    converted_number = hexa_to_dec(number_to_convert)
                if numbers_and_bases[0][1] == "Binaire":
                    converted_number = hexa_to_bin(number_to_convert)

            converted_number = str(converted_number)
            second_entry.delete(0,END)
            second_entry.insert(0,converted_number)

        # Nombres invalides (décimal et binaire)
        except ValueError:
            summon_error_window()
        # Nombres invalides (hexadécimal)
        except KeyError:
            summon_error_window()
        # Fix pour bug conversion binaire/binaire avec valeurs invalides
        except UnboundLocalError:
            summon_error_window()

# Convertir de droite à gauche
def convert_second_to_first():
    numbers_and_bases = get_numbers_and_bases()
    number_to_convert = numbers_and_bases[1][1]

    # Vérifie si le nombre à convertir n'est pas vide et affiche la fenêtre d'erreur si oui
    if bool(number_to_convert.strip()) == False:
        summon_error_window()

    else:
        try:
            if numbers_and_bases[0][1] == "Décimal":
                number_to_convert = int(number_to_convert)
                if numbers_and_bases[0][0] == "Binaire":
                    converted_number = dec_to_bin(number_to_convert)
                if numbers_and_bases[0][0] == "Hexadécimal":
                   converted_number = dec_to_hexa(number_to_convert)

            if numbers_and_bases[0][1] == "Binaire":
                if numbers_and_bases[0][0] == "Décimal":
                    converted_number = bin_to_dec(number_to_convert)
                if numbers_and_bases[0][0] == "Hexadécimal":
                    converted_number = bin_to_hexa(number_to_convert)

            if numbers_and_bases[0][1] == "Hexadécimal":
                if numbers_and_bases[0][0] == "Décimal":
                    converted_number = hexa_to_dec(number_to_convert)
                if numbers_and_bases[0][0] == "Binaire":
                    converted_number = hexa_to_bin(number_to_convert)

            converted_number = str(converted_number)
            first_entry.delete(0,END)
            first_entry.insert(0,converted_number)

        # Nombres invalides (décimal et binaire)
        except ValueError:
            summon_error_window()
        # Nombres invalides (hexadécimal)
        except KeyError:
            summon_error_window()
        # Fix pour bug conversion binaire/binaire avec valeurs invalides
        except UnboundLocalError:
            summon_error_window()

# Configuration de l'interface graphique de la fenêtre principale
gui = Tk()
gui.title("NCI")
gui.geometry("263x110")
gui.resizable(0, 0)
icon_small = PhotoImage(file="./src/icon-16.png")
icon_big = PhotoImage(file="./src/icon-32.png")
gui.iconphoto(True, icon_small, icon_big)

# Arrière-plan
background = PhotoImage(file='./src/bg.png')
background_label = Label(gui, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Menu des bases
bases = ["Décimal", "Binaire", "Hexadécimal"]
first_menu = ttk.Combobox(gui, values=bases, width=12, state="readonly")
second_menu = ttk.Combobox(gui, values=bases, width=12, state="readonly")

first_menu['values'] = ("Décimal", "Binaire", "Hexadécimal")
second_menu['values'] = ("Décimal", "Binaire", "Hexadécimal")

# Options par défaut pour le menu
first_menu.current(0)
second_menu.current(1)

first_entry = Entry(gui, width=12, bg= '#000000', fg='#00d52e')
second_entry = Entry(gui, width=12, bg= '#000000', fg='#00d52e')

# Bouttons
btn_frame = Frame(gui)
btn_left_to_right = Button(btn_frame, text=">>>", height=1, bd=1, command=convert_first_to_second)
btn_right_to_left = Button(btn_frame, text="<<<", height=1, bd=1, command=convert_second_to_first)
btn_left_to_right.pack(side=TOP)
btn_right_to_left.pack(side=BOTTOM)

# Placement des widgets
first_menu.grid(row=1, column=0, padx=10, pady=10)
second_menu.grid(row=1, column=2, padx=10, pady=10)
first_entry.grid(row=2, column=0)
second_entry.grid(row=2, column=2)
btn_frame.grid(row=2, column=1, pady=10)

# Boucle infinie
gui.mainloop()
