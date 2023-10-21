# conversion : Module pour conversion-CLI.py et conversion-GUI.py
# Par Nolan CACERES VASQUEZ et Merwan DE LA PENA TORTELLIER

## Décimal -> Binaire
def dec_to_bin(decimal):
    """
    dec_to_bin : convertit décimal en binaire
    Arguments :
    - decimal : entier
    Renvoie :
    - binaire : chaîne de caractères
    """

    chiffres_bin = []
    while True:
        quotient = decimal // 2
        reste = decimal % 2
        chiffres_bin.insert(0, str(reste)) # str(reste) pour que ''.join fonctionne

        if quotient == 0:
            break

        decimal = quotient
    return ''.join(chiffres_bin)

## Décimal -> Hexadécimal
def dec_to_hexa(decimal):
    """
    dec_to_hexa : convertit décimal en hexadécimal
    Arguments :
    - decimal : entier
    Renvoie :
    - hexadecimal : chaîne de caractères
    """

    dict_chiffres_dec_hexa = {
        "0" : "0",
        "1" : "1",
        "2" : "2",
        "3" : "3",
        "4" : "4",
        "5" : "5",
        "6" : "6",
        "7" : "7",
        "8" : "8",
        "9" : "9",
        "10" : "A",
        "11" : "B",
        "12" : "C",
        "13" : "D",
        "14" : "E",
        "15" : "F"
    }

    chiffres_hexa = []

    while True:
        quotient = decimal // 16
        reste = decimal % 16
        chiffres_hexa.insert(0, dict_chiffres_dec_hexa[str(reste)])

        if quotient == 0:
            break

        decimal = quotient
    return ''.join(chiffres_hexa)

## Binaire -> Décimal
def bin_to_dec(binaire):
    """
    bin_to_dec : convertit binaire en décimal
    Arguments :
    - binaire : chaîne de caractères
    Renvoie :
    - Entier
    """

    # Vérifie si il s'agit d'un nombre binaire valide, déclenche une exception sinon
    chiffres_invalides = ["2", "3", "4", "5", "6", "7", "8", "9"]
    for chiffre in chiffres_invalides:
        if chiffre in binaire:
            raise ValueError("Chiffres invalides")

    binaire = binaire[::-1] # Corrige l'ordre
    decimal = 0
    for i in range(len(binaire)):
        decimal += int(binaire[i])*2**i

    return decimal

## Binaire -> Hexadécimal
def bin_to_hexa(binaire):
    """
    bin_to_hexa : convertit binaire en hexadécimal
    Arguments :
    - binaire : chaîne de caractères
    Renvoie :
    - hexadecimal : chaîne de caractères
    """

    decimal = bin_to_dec(binaire)
    hexadecimal = dec_to_hexa(decimal)
    return hexadecimal

## Hexadécimal -> Décimal
def hexa_to_dec(hexadecimal):
    """
    hexa_to_dec : convertit hexadécimal en décimal
    Arguments :
    - hexadecimal : chaîne de caractères
    Renvoie :
    - decimal : entier
    """
    chiffres_hexa = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15
    }
    hexadecimal = hexadecimal[::-1].upper() # Corrige l'ordre et permet d'ignorer la casse
    decimal = 0
    for i in range(len(hexadecimal)):
        decimal += chiffres_hexa[hexadecimal[i]]*16**i

    return decimal

## Hexadécimal -> Binaire
def hexa_to_bin(hexadecimal):
    """
    hexa_to_bin : convertit hexadécimal en binaire
    Arguments :
    - hexadecimal : chaîne de caractères
    Renvoie :
    - binaire : chaîne de caractères
    """
    decimal = hexa_to_dec(hexadecimal)
    binaire = dec_to_bin(decimal)
    return binaire
