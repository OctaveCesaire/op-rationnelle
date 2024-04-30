# Importation
import numpy as np  # Pour les matrices
from sympy import symbols, Eq, solve #Calcul des potentienls

# Lecture de fichier OK
def readingFile(file):
    with open(file) as f:
        FileContent = f.readlines()
        # data table initialize
        data, count = [], []

        # Conversion des lignes en entier et en tableau de tableau: [[],[],[]] withdout first line
        for el in FileContent:
            dt = [int(elt) for elt in el.strip().split()]
            data.append(dt)
        count, order = data[0], data[-1]
        data.pop(0)
        data.pop(-1)
        if [len(data), len(data[0]) - 1] == count:
            return data, order
    f.close()

# Afficher la matrice de donnnees
def printMatrice(message,data):
    print(message)
    for elt in data:
        for el in elt:
            if 0<= el <= 9:
                print(el, end="  |")
            elif 10 <= el <= 99:
                print(el,end=" |")
            else:
                print(el,end="|")
        print()

# Choice the first algo that he would like run firstly
def choiceAlgo():
    choice = int(input("Choisissez un algorithme :\n1- Nord-Ouest\n2- Balas-Hammer\nResponse : "))
    match choice:
        case 1:
            print("Algorithme that run now is  form Nord-Ouest")
        case 2:
            print("Algorithme that run now is  form Balas-Hammer")
        case _:
            print("NULL")

# Graphe Initial pour Algo de Balas-Hammer
def graphInit(data, order):
    order.append(0)
    rest = np.vstack((data, order))
    return rest

# Calcul de Potentiel OK
def CalculPotentiel(graph, s,a, c):  # Graph : Celui obbtenu apres la methode 1 ou 2

    var, i, systemEquation = '', 0, []
    for sommet in s:
        var += 'S' + str(sommet) + ' '
    for commande in c:
        var += 'C' + str(commande) + ' '

    while i < a:
        S_var = symbols('S' + str(graph[0][i]))  # Créer un symbole pour S
        C_var = symbols('C' + str(graph[1][i]))  # Créer un symbole pour C
        equation = Eq(S_var - C_var, graph[2][i])  # Construire l'équation
        systemEquation.append(equation)  # Ajouter l'équation à la liste
        i += 1
    systemEquation.append(Eq(symbols('C' + str(graph[1][0])), 0))
    solution = solve(systemEquation, symbols(var))
    return solution

# Extrait les cout du graph initial @data : graph
def costInit(data):
    return data[0:data.shape[0], :- 1]

#Calcul des cout marginaux OK
def costMargi(res, solutionPotenti):  # res graphe initial sans a derni7re ligne et coloone
    n, m = res.shape
    graphPotent = np.zeros((n, m))
    for i in range(0, n):
        for j in range(0, m):
            p_i_j = solutionPotenti[symbols('S' + str(i))] - solutionPotenti[symbols('C' + str(j))]
            graphPotent[i, j] = (p_i_j - res[i, j])
            graphPotent = graphPotent.astype(int)
    return graphPotent  # Envoie de la matrice de coup matrginaux

# Function qui retourne les sommet, nbre d'arrête, les commandes
def graphNature(ext,init):
    s,c,graph_phy,a = [],[],[[],[],[]],0 # s*c*graph_phy*a : sommet*commande*graphe*arrêt
    line, col = ext.shape
    for i in range(line):
        for j in range(col):
            if ext[i,j] != 0:
                graph_phy[0].append(i)#Source
                graph_phy[1].append(j)#commande
                graph_phy[2].append(init[i,j])
                if i not in s:
                    s.append(i)
                if j not in c:
                    c.append(j)
                a += 1
    res = [True if (ext.shape == (len(s), len(c)) and a == len(s) + len(c) - 1) else False,a, s, c]
    #print("graph_phy : ",graph_phy)
    return graph_phy,res

#Séletionner la case avec le cout marginal près faible
def recupurer_zone_add(coutMarginaux):
    zones_slt = []
    n, m = coutMarginaux.shape
    for i in range(n):
        for j in range(m):
            if coutMarginaux[i,j] < 0:
                zones_slt.append([i,j,abs(coutMarginaux[i,j])])

    max_third_element = max([tableau[2] for tableau in zones_slt])
    premier_tableau_max = None
    for tableau in zones_slt:
        if tableau[2] == max_third_element:
            premier_tableau_max = tableau
            break  # Sortir de la boucle une fois que le premier est trouvé

    return premier_tableau_max

# Ramener les donnéer en format dictionnaire
def adjacency_list(edge):
    graph ={}
    for i in range(len(edge[0])):
        source = edge[1][i]# Commande
        destination = edge[0][i]# Source
        if source not in graph:
            graph[source] = [destination]
        else:
            graph[source].append(destination)
    return graph

#def detectionCycle(graph,sommet,column):
def detectionCycle(graph,n,m):
    circuit = np.empty((n, m), dtype=object)  # Utilisation de dtype=object pour permettre des tuples de différentes tailles
    # Initialisation du circuit remplir de -1
    for i in range(n):
        for j in range(m):
            circuit[i, j] = (-1, -1)

    for C in graph:
        for S in graph[C]:
            circuit[C,S] = (C,S)

    formatted,cycle_found = [],[]

    #Ramener le circuit à un tableau de tableau
    for row in circuit:
        formatted_row = [tuple(cell) for cell in row]
        formatted.append(formatted_row)

    for i in range(3):
        for j in range(4):
            sous_matrice = [row[j:j + 2] for row in formatted[i:i + 2]]
            if len(sous_matrice) >= 2 and sum(len(ligne) for ligne in sous_matrice) == 4:
                contient_pas = all(element != (-1, -1) for ligne in sous_matrice for element in ligne)
                if contient_pas:
                    cycle_found.extend(element for ligne in sous_matrice for element in ligne)

    return cycle_found

#Marche pied en cas de présence de cycel
def marchePied(graphPhy,ext,n,m):
    # Créer un graphe de dictionnaire
    graphCor = adjacency_list([graphPhy[0], graphPhy[1]])
    dictionnaire = {40: [0, 1, 2], 51: [1, 2, 3], 32: [3]}
    # Vérifier si il il y a un cycle après ajout de l'arrêt de coût de marginal négatif
    cycleFound = detectionCycle(graphCor, n,m)
    ValDuCycle = {}
    for el in cycleFound:
        source = ext[el[1], el[0]]
        ValDuCycle[source] = el
    key_filtres = [key for key in ValDuCycle.keys() if key != 0]
    petit_lambda = min(key_filtres)
    alt = True
    for el in cycleFound:
        if alt:
            ext[el[1], el[0]] =  abs(ext[el[1], el[0]] - petit_lambda)
        else:
            ext[el[1], el[0]] = abs(ext[el[1], el[0]] + petit_lambda)

        alt = not alt
    return ext

#Affichage du graphe
def TraceGraph(graph,message):
    print("\nTracé du graphe",message)
    i = 0
    print(" P | C : Cout")
    while i < len(graph[0]):
        print(f'P{graph[0][i]}->C{graph[1][i]} : cout {graph[2][i]}',end="\n")
        i += 1

def Afficher_Cycle(cycle,message):
    print("\nAffichage du cycle present dans le graphe",message)
    for c,s in cycle:
        print(f'C{c} -> S{s}')

# Algo de controle générale pour le cout marginal
def controle_globale(coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti):

    while np.any(coutMarginaux < 0):
        print("\nIl y a des valeur négatif dans la matrice de coûts marginale.\n\nAjout d'une nouvelle arrête à la proposition initiale.")

        case_slt = recupurer_zone_add(coutMarginaux)
        graph[0].append(case_slt[0])
        graph[1].append(case_slt[1])
        graph[2].append(case_slt[2])
        TraceGraph(graph,"secondaire")

        cycle = detectionCycle(adjacency_list(graph), nbreCommande, nbreSource)

        if cycle != []:
            Afficher_Cycle(cycle,"secondaire")

            sortie = marchePied(graph, sortie, nbreCommande, nbreSource)

            graph, b = graphNature(sortie, cout_inti)
            printMatrice("\nAprès application de la méthode marche-pied.\n\nVoici la nouvelle proposition de solution",sortie)

            potentielSourceCommande = CalculPotentiel(graph, b[2], nbrArret, b[3])

            print("\nRecalculable des nouvelle potentielle:\n",potentielSourceCommande)
            coutMarginaux = costMargi(cout_inti, potentielSourceCommande)
            printMatrice("\nCalcul des coûts marginaux", coutMarginaux)

            #print("\nCalcul des coûts marginaux:\n", coutMarginaux)
        else:
            print("Le graphe est correcte")
        break

    return coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti
##