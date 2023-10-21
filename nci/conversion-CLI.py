# Numerical
# Conversion
# Interface
# Version CLI
# Par Nolan CACERES VASQUEZ et Merwan DE LA PENA TORTELLIER

from conversion import *
from os import system as command
from platform import system

ascii_logo = '''===================

mm   m   mmm  mmmmm 
#"m  # m"   "   #   
# #m # #        #   
#  # # #        #   
#   ##  "mmm" mm#mm

===================\n'''

# Utilisation de la bonne commande pour vider l'écran
clear_commands = {"Windows": "cls",
                  "Linux": "clear",
                  "Darwin": "clear"}
clear = clear_commands[system()]

# Valeurs par défaut
bases_listes = ["Base 10 (Décimal)", "Base 2 (Binaire)", "Base 16 (Hexadécimal)"]
base_origine_index = None
base_converti_index = None
current_mode = 0

while True:
    # Sélection de la base d'origine
    if current_mode == 0:
        command(clear)
        print(ascii_logo)
        print("Pressez Ctrl-C pour quitter\n")
        print("Choisissez votre base d'origine")
        
        # Affiche la liste des bases
        index_liste = []
        for position in range(len(bases_listes)):
            print(f'{position+1}: {bases_listes[position]}')
            index_liste.append(position)
        
        while True:
            # Demande la base d'origine et vérifie si le choix est valide
            try:
                base_origine_index = int(input("Choix : "))-1
                if not base_origine_index in index_liste:
                    raise ValueError
                current_mode = 1
                break
            except ValueError:
                print("Choix invalide")
            except KeyboardInterrupt: # Si Ctrl-C pressé : Quitte le programme
                exit()
    
    # Sélection de la base de destination
    if current_mode == 1:
        command(clear)
        print(ascii_logo)
        print("Pressez Ctrl-C pour revenir au menu précédent\n")
        print("Choisissez votre base de destination")
        
        # Affiche la liste des bases SAUF la base qui a été choisie précédemment
        index_liste = []
        for position in range(len(bases_listes)):
            if bases_listes[base_origine_index] != bases_listes[position]:
                print(f'{position+1}: {bases_listes[position]}')
                index_liste.append(position)
    
        while True:
            # Demande la base pour le nombre converti et vérifie si le choix est valide
            try:
                base_converti_index = int(input("Choix : "))-1
                if not base_converti_index in index_liste:
                    raise ValueError
                current_mode = 2
                break
            except ValueError:
                print("Choix invalide")
            # Si Ctrl-C pressé : Reviens au menu précédent
            except KeyboardInterrupt:
                current_mode = 0
                break

    
    # Conversion
    if current_mode == 2:
        command(clear)
        print(ascii_logo)
        print("Pressez Ctrl-C pour revenir au menu précédent\n")

        while True:
            try:
                # Demande le nombre à convertir
                nb_a_convertir = input(f"Nombre en {bases_listes[base_origine_index]} à convertir : ")
                nb_converti = None

                if base_origine_index == 0: # Décimal -> ...
                    nb_a_convertir = int(nb_a_convertir)
                    if base_converti_index == 1: # Décimal -> Binaire
                        nb_converti = dec_to_bin(nb_a_convertir)
                    if base_converti_index == 2: # Décimal -> Hexadécimal
                        nb_converti = dec_to_hexa(nb_a_convertir)
                
                if base_origine_index == 1: # Binaire -> ...
                    if base_converti_index == 0: # Binaire -> Décimal
                        nb_converti = bin_to_dec(nb_a_convertir)
                    if base_converti_index == 2: # Binaire -> Hexadécimal
                        nb_converti = bin_to_hexa(nb_a_convertir)
                
                if base_origine_index == 2: # Hexadécimal -> ...
                    if base_converti_index == 0: # Hexadécimal -> Décimal
                        nb_converti = hexa_to_dec(nb_a_convertir)
                    if base_converti_index == 1: # Hexadécimal -> Binaire
                        nb_converti = hexa_to_bin(nb_a_convertir)

                # Affiche le nombre converti
                print(f"Nombre converti en {bases_listes[base_converti_index]} : {nb_converti}")

            # Message d'erreur pour nombre invalide
            except ValueError:
                print("Nombre invalide!") # Décimal et Binaire
            except KeyError:
                print("Nombre invalide!") # Hexadécimal

            # Si Ctrl-C pressé : Reviens au menu précédent
            except KeyboardInterrupt:
                current_mode = 1
                break
            