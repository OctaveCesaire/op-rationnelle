# Importation
from Fonctions import printMatrice,graphNature,TraceGraph,detectionCycle,adjacency_list,CalculPotentiel,costMargi,controle_globale,RemplissageBalas

def BalasHammer(graphinitial,cout_inti):

    sortie,graphinitial = RemplissageBalas(graphinitial)

    printMatrice("\nAlgorithme that run now is  form Balas Hammer:",sortie)

    graph, b = graphNature(sortie,cout_inti)
    TraceGraph(graph,"initial")
    nbrArret,nbreSource,nbreCommande = b[1],len(b[2]),len(b[3])

    cycle = detectionCycle(adjacency_list(graph),nbreCommande,nbreSource)
    #print("cycle :",cycle)
    print("nbreCommande + nbreSource == nbrArret + 1:",nbreCommande + nbreSource == nbrArret + 1)

    if cycle == [] and nbreCommande + nbreSource == nbrArret + 1:
        print("\nLe graphe est acyclique et connexe.\n\nCalcul des potentiels de chaque Source et Commande:\n")
        potentielSourceCommande = CalculPotentiel(graph,b[2],nbrArret,b[3])
        print("Potentiel de chaque Source et Commande du graphe initial:\n",potentielSourceCommande)
        coutMarginaux = costMargi(cout_inti,potentielSourceCommande)
        printMatrice("\nCalcul des coûts marginaux",coutMarginaux)
        print("graph :",graph)
        coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti = controle_globale(coutMarginaux,sortie, graph, nbreCommande, nbreSource, graphinitial, nbrArret, cout_inti)
        TraceGraph(graph,"optimale")
    else:
        ### Suite à voir au cas où le grphe est dégénére
        print("Nombre d'arrêt :",nbrArret,"Nombre de source inclus dans le graphe: ", nbreSource,"Nombre de commande inclus dans le graph :",nbreCommande)
        print("\nLe graphe n'est ni connexe ni acyclique ")