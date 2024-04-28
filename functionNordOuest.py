# Importation
import numpy as np# Pour les matrices

# Algo Nord-Ouest
def RemplassageNordOuset(data):
    ext = np.full((data.shape[0]-1,data.shape[1]-1),-1)
    i = 0
    while i < data.shape[0] -1:
        row = data[i]
        j = 0
        while j < data.shape[1] -1:
            col = data[:,j]
            ext[i,j] = min(row[-1],col[-1])
            row[-1] = row[-1] - ext[i,j]
            data[i] = row
            col[-1] = col[-1] -ext[i,j]
            data[:,j] = col
            j += 1
        i += 1
    return ext

