
import numpy as np
import scipy
from scipy.sparse import lil_matrix
from scipy.sparse import linalg
import cv2

def on_omega(point, omega):
    if omega[point] != 1:
        return False
    i,k = point
    border = [(i+1,k),(i-1,k),(i,k+1),(i,k-1)]
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
    #print(len(pointss))
    print(pointss[0])
    matrix = scipy.sparse.lil_matrix((len(points[0]),len(points[0])),dtype=np.float64)
    print(matrix.shape)
    for i in enumerate(pointss):
        #print(i[1][0])
        matrix[i[1][0], i[1][0]] = 4.0
        x = i[1][0]
        y = i[1][1]
        border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for point in border:
            if point in pointss:
                index = pointss.index(point)
                matrix[i[1][0], index] = -1
    print("finished creating sparse matrix!!")
    #matrix = lil_matrix(matrix)
    return matrix


def poisson_blend(source, target, mask):    
    nonzero = np.nonzero(mask)
    
    points = list(zip(nonzero[0], nonzero[1]))
    print(len(points))
    matrixA = create_sparse_matrix(nonzero)
    matrixB = np.zeros(len(points))
    for i, k in enumerate(points):
        x,y = k
        matrixB[i] = -4*source[x,y] + source[x+1,y] + source[x-1,y] + source[x,y+1] + source[x,y-1]
        if point_area(k, mask) == 1:
            border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            for p in border:
                if mask[p] == False:
                    matrixB[i] = matrixB[i] + target[p]
    
    unknown_values = linalg.cg(matrixA, matrixB)
    #print(unknown_values)
    #print(target)
    composite = np.copy(target).astype(int)
    for i, k in enumerate(points):
        composite[k] = unknown_values[0][i]
    return composite
    


if __name__ == "__main__":
    source_name = "dog.png"
    target_name = "beach.png"
    mask_name = "mask1.png"
    '''source_name = input("Enter file name of source image ")
    target_name = input("Enter file name of target image ")
    mask_name = input("Enter file name of mask ")'''

    source_image = cv2.imread(source_name)
    target_image = cv2.imread(target_name)
    mask_image = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)

    

    mask = np.atleast_3d(mask_image).astype(float)/255
    source = np.atleast_3d(source_image).astype(float)/255
    target = np.atleast_3d(target_image).astype(float)/255
    source = np.atleast_3d(source_image)
    target = np.atleast_3d(target_image)
    mask[mask != 1] = 0
    mask = mask[:,:,0]
    print(len(mask))
    print(len(mask[0]))
    
    #RGBchannels = np.array(source_image).astype(int)
    #print(len(RGBchannels))
    results = []
    for channel in range(len(target)):
        results.append(poisson_blend(source[:,:,channel], target[:,:,channel], mask))

    result = cv2.merge(results)
    cv2.imwrite("output.png",result)

