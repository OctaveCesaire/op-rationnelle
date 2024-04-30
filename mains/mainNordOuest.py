#Importation
from Fonctions import marchePied,printMatrice,graphNature,TraceGraph,detectionCycle,adjacency_list,CalculPotentiel,costMargi,controle_globale,RemplassageNordOuset

def NordOuest(graphinitial,cout_inti):
    sortie = RemplassageNordOuset(graphinitial)
    printMatrice("\nAlgorithme that run now is  form Nord-Ouest:",sortie)

    graph, b = graphNature(sortie,graphinitial)
    TraceGraph(graph,"initial")

    nbrArret,nbreSource,nbreCommande = b[1],len(b[2]),len(b[3])
    cycle = detectionCycle(adjacency_list(graph),nbreCommande,nbreSource)

    if cycle == [] and nbreCommande + nbreSource == nbrArret + 1:
        print("\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n")
        potentielSourceCommande = CalculPotentiel(graph,b[2],nbrArret,b[3])
        print("Potentiel de chaque Source et Commande du graphe initial:\n",potentielSourceCommande)
        coutMarginaux = costMargi(cout_inti,potentielSourceCommande)
        printMatrice("\nCalcul des coûts marginaux",coutMarginaux)
        coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti = controle_globale(coutMarginaux,sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti)
        TraceGraph(graph,"optimale")
    else:
        ### Suite à voir au cas où le grphe est dégénére
        if cycle != []:
            sortie = marchePied(graph, sortie, nbreCommande, nbreSource)
            graph, b = graphNature(sortie, cout_inti)
            printMatrice("\nAprès application de la méthode marche-pied.\n\nVoici la nouvelle proposition de solution",sortie)

            potentielSourceCommande = CalculPotentiel(graph, b[2], nbrArret, b[3])

            print("\nCalcul des potentielles:\n", potentielSourceCommande)
            coutMarginaux = costMargi(cout_inti, potentielSourceCommande)
            printMatrice("\nCalcul des coûts marginaux", coutMarginaux)
        else:
            print("\nLe graphe dégénéré. ")
            TraceGraph(graph,"Dégénéré")
            print("Nombre d'arrêt :",nbrArret,"Nombre de sommets dans le graphe: ", nbreSource + nbreCommande)