import numpy as np# Pour les matrices

#Calcul de pénalité
def calculPenality(grap_retire_zone_done):
    n, m = grap_retire_zone_done.shape
    penalityRow, penalityCol, index_row_done, index_col_done = [], [], [], []

    # Row
    for i in range(n - 1):
        dailLine, selt_line = grap_retire_zone_done[i, -1],grap_retire_zone_done[i]
        if dailLine == -1:
            penalityRow.append(-1)
            index_row_done.append(i)
        else:
            penalityRow.append(retirer_Ligne_Colonne(selt_line))

    # Colonne
    for j in range(m - 1):
        dailCol, selt_col = grap_retire_zone_done[-1, j], grap_retire_zone_done[:, j]
        if dailCol == -1:
            penalityCol.append(-1)
        else:
            penalityCol.append(retirer_Ligne_Colonne(selt_col))
    return penalityRow, penalityCol

# Retirer la ligne ou la colonne
def retire_zone_done(data):
    n, m = data.shape
    cop_dat = data
    for i in range(n):
        line = cop_dat[i]
        if line[-1] == -1:
            cop_dat[i] = np.full((1,m),-1)

    for j in range(m):
        col = cop_dat[:,j]
        if col[-1] == -1:
            cop_dat[:,j] = np.full((1,n),-1)
    return  cop_dat

# Choix de la zone
def choiceAera(row,col):
    max_row = max(enumerate(row),key=lambda x:x[1])
    max_col = max(enumerate(col),key=lambda x:x[1])
    return max_row, max_col

# Calcul De pénalité
def retirer_Ligne_Colonne(tableau):
    tabl = []
    penality = 0
    for i in tableau:
        if i != -1:
            tabl.append(i)
    tabl.pop(-1)
    if len(tabl) > 1:
        for nbr in range(2):
            penality = abs(penality - min(tabl))
            tabl.pop(tabl.index(min(tabl)))
    elif len(tabl) == 0:
        penality = -1 # Fin des calcul de pénalité
    else :
        penality = tabl[0]
    return penality

# Remplir la matrice init
def RemplissageBalas(graph):
    graphinit = graph
    provision, commande = graphinit[-1][graphinit[-1] != 0], graphinit[:, -1][graphinit[:, -1] != 0]
    n, m = graphinit.shape

    elt = np.full((n - 1, m - 1), 0)

    while (np.any(provision != -1) or np.any(commande != -1)):
        penality_row, penality_col = calculPenality(retire_zone_done(graphinit))
        max_penality_row, max_penality_col = choiceAera(penality_row, penality_col)

        if max_penality_row[1] < max_penality_col[1]:
            choix_col = max_penality_col[0]
            grap_col = graphinit[:, choix_col]

            if min(enumerate(graphinit[:-1, choix_col]), key=lambda x: x[1])[1] != -1:
                choix_row, val = min(enumerate(graphinit[:-1, choix_col]), key=lambda x: x[1])
            else:
                grap_col[grap_col == -1] = np.max(grap_col)
                choix_row, val = min(enumerate(graphinit[:-1, choix_col]), key=lambda x: x[1])
            elt[choix_row, choix_col] = min(graphinit[choix_row, -1], grap_col[-1])

            graphinit[choix_row, -1] -= elt[choix_row, choix_col]
            if graphinit[choix_row, -1] == 0:
                graphinit[choix_row, -1] = -1

            graphinit[-1, choix_col] -= elt[choix_row, choix_col]

            if graphinit[-1, choix_col] == 0:
                graphinit[-1, choix_col] = -1

        else:
            choix_row = max_penality_row[0]
            grap_row = graphinit[choix_row]

            if min(enumerate(graphinit[choix_row,:-1]), key=lambda x: x[1])[1] != -1:
                choix_col, val = min(enumerate(graphinit[choix_row,:-1]), key=lambda x: x[1])
            else:
                grap_row[grap_row == -1] = np.max(grap_row)
                choix_col, val = min(enumerate(graphinit[choix_row,:-1]), key=lambda x: x[1])
            elt[choix_row, choix_col] = min(graphinit[choix_row, -1], graphinit[-1, choix_col])

            graphinit[choix_row, -1] -= elt[choix_row, choix_col]

            if graphinit[choix_row,-1] == 0:
                graphinit[choix_row, -1] = -1

            graphinit[-1, choix_col] -= elt[choix_row, choix_col]

            if graphinit[-1, choix_col] == 0:
                graphinit[-1, choix_col] = -1

        provision, commande = graphinit[-1][graphinit[-1] != 0], graphinit[:, -1][graphinit[:, -1] != 0]
    cop_grap = graph
    return elt,cop_grap
