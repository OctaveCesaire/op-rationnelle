# Importation
from Fonctions import marchePied,printMatrice,graphNature,TraceGraph,detectionCycle,adjacency_list,CalculPotentiel,costMargi,controle_globale,RemplissageBalas

def BalasHammer(graphinitial,cout_inti,f):

    sortie,graphinitial = RemplissageBalas(graphinitial)
    printMatrice("\nAlgorithme that run now is  form Balas Hammer:",sortie,f)
    graph, b = graphNature(sortie,cout_inti)
    TraceGraph(graph,"initial",f)
    nbrArret,nbreSource,nbreCommande = b[1],len(b[2]),len(b[3])
    cycle = detectionCycle(adjacency_list(graph),nbreCommande,nbreSource)

    if cycle == [] and nbreCommande + nbreSource == nbrArret + 1:
        print("\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n")
        f.write(f'\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n')
        potentielSourceCommande = CalculPotentiel(graph,b[2],nbrArret,b[3])
        print("Potentiel de chaque Source et Commande du graphe initial:\n",potentielSourceCommande)
        f.write(f'\nPotentiel de chaque Source et Commande du graphe initial:\n{potentielSourceCommande}')
        coutMarginaux = costMargi(cout_inti,potentielSourceCommande)
        printMatrice("\nCalcul des coûts marginaux",coutMarginaux,f)
        coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti = controle_globale(coutMarginaux,sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti,f)
        TraceGraph(graph,"optimale",f)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    else:
        ### Suite à voir au cas où le grphe est dégénére
        if cycle != []:
            sortie = marchePied(graph, sortie, nbreCommande, nbreSource)
            graph, b = graphNature(sortie, cout_inti)
            printMatrice("\nAprès application de la méthode marche-pied.\n\nVoici la nouvelle proposition de solution",
                         sortie, f)
            potentielSourceCommande = CalculPotentiel(graph, b[2], nbrArret, b[3])
            print("\nCalcul des potentielles:\n", potentielSourceCommande)
            f.write(f'\nCalcul des potentielles:\n{potentielSourceCommande}')
            coutMarginaux = costMargi(cout_inti, potentielSourceCommande)
            printMatrice("\nCalcul des coûts marginaux", coutMarginaux, f)
            coutMarginaux, sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti = controle_globale(
                coutMarginaux, sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti, f)
            TraceGraph(graph, "optimale", f)
        else:
            print("\nLe graphe est dégénéré. ")
            f.write(f'\nLe graphe est dégénéré. \n')
            TraceGraph(graph, "Dégénéré", f)
            print("Nombre d'arrêt :", nbrArret, "Nombre de sommets dans le graphe: ", nbreSource + nbreCommande)