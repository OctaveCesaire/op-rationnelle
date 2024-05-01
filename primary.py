#Importation
from Fonctions import writingFile

Exit = "y"
while Exit != "n" :
    test = None

    while test not in ['1','2','3','4','5','6','7','8','9','10','11','12']:
        test = input("Choisissez le fichier test à éxecuter entre 1 à 12 : ")

    writingFile(test)
    Exit = input("Vouliez-vous poursuivre? (Y/n) :").lower()

    while Exit not in ["y","n"]:
        print("Mauvais choix.")
        Exit = input("Vouliez-vous poursuivre? (Y/n) :").lower()