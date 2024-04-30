#Importation
from Fonctions import readingFile,graphInit,printMatrice,costInit,np
from Mains.mainBalasHammer import BalasHammer
from Mains.mainNordOuest import NordOuest

Exit = "y"

while Exit != "n" :
    dt, commande = readingFile("text.txt")
    cout_inti = costInit(np.array(dt))
    graphinitial = graphInit(dt, commande)
    printMatrice("\nAffichage du graphe initial:", graphinitial)

    choice = 3
    while choice not in [ 1, 2]:
        choice = int(input("Choisissez un algorithme :\n1- Nord-Ouest\n2- Balas-Hammer\nResponse : "))

    match choice:
        case 1:
            NordOuest(graphinitial, cout_inti)
        case 2:
            BalasHammer(graphinitial, cout_inti)
        case _:
            print("Fin du programme")

    Exit = input("Vouliez-vous poursuivre? (Y/n) :").lower()

    if Exit not in ["y","n"]:
        print("Mauvais choix.")
        Exit = input("Vouliez-vous poursuivre? (Y/n) :").lower()