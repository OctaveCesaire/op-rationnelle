from .functionNordOuest import *
from .functionBalasHammer import *
from .generalFunction import *
from Mains.mainBalasHammer import *
from Mains.mainNordOuest import *

import time
import cProfile

## Ecriture dans Fichier
def writingFile(file):
    directory_path_writing = f'./Tracées/tracée{file}.txt'
    with open(directory_path_writing,'a+') as f:
        dt, commande = readingFile(file)
        cout_inti = costInit(np.array(dt))
        graphinitial = graphInit(dt, commande)
        printMatrice("\nAffichage du graphe initial:", graphinitial,f)

        choice = 3
        while choice not in [1, 2]:
            choice = int(input("Choisissez un algorithme :\n1- Nord-Ouest\n2- Balas-Hammer\nResponse : "))
        match choice:
            case 1:
                NordOuest(graphinitial, cout_inti, f)
            case 2:
                BalasHammer(graphinitial, cout_inti, f)
            case _:
                print("Fin du programme")