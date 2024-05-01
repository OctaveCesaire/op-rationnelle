#Importation
from Fonctions import marchePied,printMatrice,graphNature,TraceGraph,detectionCycle,adjacency_list,CalculPotentiel,costMargi,controle_globale,RemplassageNordOuset
import numpy as np

######################## CODE A REVOIR ##############################################
def ConversionToConnexe(edge,CostInt):
 #   edge = [[0, 1, 2, 3, 4, 5, 6], [0, 0, 0, 0, 1, 1, 2], [30, 10, 9, 6, 40, 38, 22]]
    CopyRetour = edge
#    CostInt = np.array([[30, 20, 15], [10, 50, 2], [9, 10, 30], [6, 2, 29], [50, 40, 3], [5, 38, 27], [50, 4, 22]])
    graph = {}
    n, m = 3, 7

    for i in range(len(edge[0])):
        source = edge[1][i]  # Commande
        destination = edge[0][i]  # Source
        if source not in graph:
            graph[source] = [destination]
        else:
            graph[source].append(destination)

    circuit, formatted = np.empty((n, m),
                                  dtype=object), []  # Utilisation de dtype=object pour permettre des tuples de différentes tailles
    for i in range(n):
        for j in range(m):
            circuit[i, j] = (-1, -1)
    for C in graph:
        for S in graph[C]:
            circuit[C, S] = (C, S)
    # Ramener le circuit à un tableau de tableau
    for row in circuit:
        formatted_row = [tuple(cell) for cell in row]
        formatted.append(formatted_row)
    print(formatted)

    ajoutArret = []
    for i in range(len(formatted) - 1):
        for j in range(len(formatted[0]) - 1):
            sub_matrix = [row[j:j + 2] for row in formatted[i:i + 2]]
            if sub_matrix[1][1] != (-1, -1) and sub_matrix[0][0] != (-1, -1) and sub_matrix[1][0] == (-1, -1):
                # Affectation de la valeur suivante à l'élément en dessous du premier élément de la première ligne
                ajoutArret.append((i + 1, sub_matrix[0][0][1]))
    for elt in ajoutArret:
        CopyRetour[0].append(elt[1])
        CopyRetour[1].append(elt[0])
        CopyRetour[2].append(CostInt[elt[1], elt[0]])

    print(
        "EDGE :", edge
    )

    print(
        'AJOUT in EDGE::', edge
    )
    return edge

#################################################################################


def NordOuest(graphinitial,cout_inti,f):
    sortie = RemplassageNordOuset(graphinitial)
    printMatrice("\nAlgorithme that run now is  form Nord-Ouest:",sortie,f)

    graph, b = graphNature(sortie,graphinitial)
    TraceGraph(graph,"initial",f)

    nbrArret,nbreSource,nbreCommande = b[1],len(b[2]),len(b[3])
    cycle = detectionCycle(adjacency_list(graph),nbreCommande,nbreSource)

    if cycle == [] and nbreCommande + nbreSource == nbrArret + 1:
        print("\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n")
        f.write(f'\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n"')
        potentielSourceCommande = CalculPotentiel(graph,b[2],nbrArret,b[3])
        print("Potentiel de chaque Source et Commande du graphe initial:\n",potentielSourceCommande)
        f.write(f'Potentiel de chaque Source et Commande du graphe initial:\n{potentielSourceCommande}')
        coutMarginaux = costMargi(cout_inti,potentielSourceCommande)
        printMatrice("\nCalcul des coûts marginaux",coutMarginaux,f)
        coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti = controle_globale(coutMarginaux,sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti,f)
        TraceGraph(graph,"optimale",f)
    else:
        ### Suite à voir au cas où le grphe est dégénére
        if cycle != []:
            sortie = marchePied(graph, sortie, nbreCommande, nbreSource)
            graph, b = graphNature(sortie, cout_inti)
            printMatrice("\nAprès application de la méthode marche-pied.\n\nVoici la nouvelle proposition de solution",sortie,f)
            potentielSourceCommande = CalculPotentiel(graph, b[2], nbrArret, b[3])
            print("\nCalcul des potentielles:\n", potentielSourceCommande)
            f.write(f'\nCalcul des potentielles:\n {potentielSourceCommande} ')
            coutMarginaux = costMargi(cout_inti, potentielSourceCommande)
            printMatrice("\nCalcul des coûts marginaux", coutMarginaux,f)
        else:
            print("\nLe graphe est dégénéré. ")
            f.write(f'\nLe graphe est dégénéré. ')
            TraceGraph(graph,"Dégénéré",f)
            print("Nombre d'arrêt :",nbrArret,"Nombre de sommets dans le graphe: ", nbreSource + nbreCommande)