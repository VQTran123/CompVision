import numpy as np
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
    matrix = np.zeros((len(points),len(points)))
    for i, k in enumerate(points):
        matrix[i, i] = -4
        x, y = k
        border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for point in border:
            if point in points:
                index = points.index(point)
                matrix[i, index] = 1
    return matrix


def poisson_blend(source, target, mask):    
    nonzero = np.nonzero(mask)
    points = list(zip(nonzero[0], nonzero[1]))
    matrixA = create_sparse_matrix(points)
    matrixB = np.zeros(len(points))
    for i, k in enumerate(points):
        x,y = k
        matrixB[i] = -4*source[x,y] + source[x+1,y] + source[x-1,y] + source[x,y+1] + source[x,y-1]
        if point_area(k, mask) == 1:
            border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            for p in border:
                if mask[p] != 1:
                    matrixB[i] = -1*matrixB[i] - target[p]
    
    unknown_values = linalg.cg(matrixA, matrixB)
    composite = np.copy(target).astype(int)
    for i, k in enumerate(points):
        composite[k] = unknown_values[0][i]
    return composite
    
def compute_gradient(image, mask):
    nonzero = np.nonzero(mask)
    points = list(zip(nonzero[0], nonzero[1]))
    gradient = np.zeros(len(points))
    for i, k in enumerate(points):
        x,y = k
        gradient[i] = int(image[x,y]) - int(image[x-1,y])
    return gradient

def compute_vector(s_grad, t_grad, mask, target):
    nonzero = np.nonzero(mask)
    points = list(zip(nonzero[0], nonzero[1]))
    vector_field =  np.copy(target).astype(int)
    for i, k in enumerate(points):
        x,y = k
        vector_field[x,y] = max(s_grad[i], t_grad[i])
        if i != 0:
            vector_field[x-1,y] = vector_field[x,y] - vector_field[x-1,y]
    return vector_field

if __name__ == "__main__":
    #source_name = "source_q1(1).jpg"
    #target_name = "target_q1(1).jpg"
    #mask_name = "phone.jpg"
    source_name = input("Enter file name of source image ")
    target_name = input("Enter file name of target image ")
    mask_name = input("Enter file name of mask ")

    source_image = cv2.imread(source_name)
    target_image = cv2.imread(target_name)
    mask_image = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)

    mask = np.atleast_3d(mask_image).astype(float)/255
    source = np.atleast_3d(source_image)
    target = np.atleast_3d(target_image)
    mask[mask != 1] = 0
    mask = mask[:,:,0]
    RGBchannels = np.atleast_1d(source_image).shape[-1]
    results = []
    for channel in range(RGBchannels):
        #Poisson w/o gradient mixing
        #results.append(poisson_blend(source[:,:,channel], target[:,:,channel], mask))
        #Gradient mixing
        source_grad = compute_gradient(source[:,:,channel], mask)
        target_grad = compute_gradient(target[:,:,channel], mask)
        results.append(compute_vector(source_grad, target_grad, mask, target[:,:,channel]))

    result = cv2.merge(results)
    cv2.imwrite("output.jpg",result)

