import numpy as np
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
    matrix = lil_matrix(len(points),len(points))
    for i, k in enumerate(points):
        matrix[i,i] = 4
        x, y = k
        border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for point in border:
            if point in points:
                index = points.index(point)
                matrix[i, index] = -1
    return matrix


def poisson_blend(source, target, mask):
    nonzero = np.nonzero(mask)
    points = zip(nonzero[0], nonzero[1])
    matrixA = create_sparse_matrix(points)
    matrixB = np.zeros(len(points))
    for i, k in enumerate(points):
        x,y = k
        laplace = -4*source[x,y] + source[x+1,y] + source[x-1,y] + source[x,y+1] + source[x,y-1]
        if point_area(k, mask) == 1:
            border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            for p in border:
                if mask[p] == False:
                    matrixB[i] = matrixB[i] + target[p]
    
    unknown_values = linalg.cg(matrixA, matrixB)
    composite = np.copy(target).astype(int)
    for i, k in enumerate(points):
        composite[k] = unknown_values[0][i]
    return composite
    


if __name__ == "__main__":
    source_name = "source_q1.jpg"
    target_name = "target_q1.jpg"
    mask_name = "mask_hw1_q1.jpg"
    '''source_name = input("Enter file name of source image ")
    target_name = input("Enter file name of target image ")
    mask_name = input("Enter file name of mask ")'''

    source_image = cv2.imread(source_name)
    target_image = cv2.imread(target_name)
    mask_image = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)

    mask = np.atleast_3d(mask_image).astype(float)/255
    source = np.atleast_3d(source_image).astype(float)/255
    target = np.atleast_3d(target_image).astype(float)/255
    mask[mask != 1] = 0
    mask = mask[:,:,0]
    RGBchannels = np.atleast_1d(source_image).shape[-1]
    results = []
    for channel in range(RGBchannels):
        results.append(poisson_blend(source[:,:,channel], target[:,:,channel], mask))

    result = cv2.merge(results)
    cv2.imwrite("output.jpg",result)

