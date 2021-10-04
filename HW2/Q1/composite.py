import numpy as np
import scipy
from scipy.sparse import linalg
import cv2

def on_omega(point, omega):
    if omega[point] != 1:
        return False
    i,k = point
    '''border = [(i+1,k),(i-1,k),(i,k+1),(i,k-1)]
    for p in border:
        if omega[p] != 1:
            return True'''
    for index in range(1):
        border = [(i+index,k),(i-index,k),(i,k+index),(i,k-index)]
        for p in border:
            if omega[p] != 1:
                return True
    return False


def point_area(point, omega):
    if omega[point] != 1:
        return 2
    elif on_omega(point, omega) == True:
        return 1
    return 0

def create_sparse_matrix(points):
    pointss = list(zip(points[0], points[1]))
    matrix = scipy.sparse.lil_matrix((len(points[0]),len(points[0])),dtype=np.float64)
    for i in enumerate(pointss):
        matrix[i[0], i[0]] = 4
        x = i[1][0]
        y = i[1][1]
        border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for point in border:
            if point in pointss:
                index = pointss.index(point)
                matrix[[index],[i[0]]] = -1
    return matrix


def poisson_blend(source, target, mask): 
    nonzero = np.nonzero(mask)
    points = list(zip(nonzero[0], nonzero[1]))
    #matrixA = create_sparse_matrix(nonzero)
    #matrixB = np.zeros(len(points))
    '''
    for i, k in enumerate(points):
        x,y = k
        matrixB[i] = 4*source[x,y] - source[x+1,y] - source[x,y+1] - source[x,y-1] - source[x-1,y]
        
        matrixB[i] = 4*source[x,y] - source[x-1,y] - source[x,y-1]
        if x + 1 < len(source[0]) and y + 1 < len(source):
            matrixB[i] = 4*source[x,y] - source[x+1,y] - source[x-1,y] - source[x,y+1] - source[x,y-1]
        elif x + 1 < len(source[0]):
            matrixB[i] = 4*source[x,y] - source[x+1,y] - source[x-1,y] - source[x,y-1]
        elif y + 1 < len(source):
            matrixB[i] = 4*source[x,y] - source[x-1,y] - source[x,y+1] - source[x,y-1]
        
        if point_area(k, mask) == 1:
            border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            for p in border:
                if mask[p] == 0:
                    matrixB[i] = matrixB[i] + target[p]
        

    test = scipy.sparse.coo_matrix(matrixA)

    matA = np.zeros((matrixA.shape))
    for i,j,v in zip(test.row, test.col, test.data):
        matA[i][j] = v
    unknown_values = np.linalg.solve(matA, matrixB)
    composite = np.copy(target).astype(float)
    for i, k in enumerate(points):
        composite[k] = unknown_values[i]
    '''
    composite = np.copy(target).astype(float)
    for i, k in enumerate(points):
        x,y = k
        if point_area(k, mask) != 1:
            composite[k] = source[k]
    composite[composite > 255] = 255
    composite[composite < 0] = 0
    return composite