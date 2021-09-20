import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse import linalg
import cv2
'''
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
        matrix[i, i] = 4
        x, y = k
        border = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for point in border:
            if point in points:
                index = points.index(point)
                matrix[i, index] = -1
    print("finished creating sparse matrix!!")
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
                if mask[p] == False:
                    matrixB[i] = matrixB[i] + target[p]
    
    unknown_values = linalg.cg(matrixA, matrixB)
    composite = np.copy(target).astype(int)
    for i, k in enumerate(points):
        composite[k] = unknown_values[0][i]
    return composite
    '''
def poisson_blend(source, target, mask):
    new_image = target.copy()
    for i in range(1,len(target)):
        for j in range(1,len(target[i])):
            if mask[i][j] == 255:
                #print (str(mask[i-1][j])+str(mask[i][j-1])+str(mask[i][j+1])+str(mask[i+1][j]))
                #print(target[i][j] + source[i][j])
                print(i)
                target[i][j] = source[i][j]
                
    
    return new_image

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

    #print (source_image[0][0])
    #print (mask_image[391][324])
    #note to self, the cv reads x and y are [y][x] with literal coord
    #print(len(source_image))
    result = poisson_blend(source_image, target_image, mask_image)
    #for i in range(1,863):
        #print(i)
        #print(" ")
        #print(str(mask_image[391][i]) + " " + str(source_image[391][i))
    '''
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
    '''
    cv2.imwrite("output.png",result)

