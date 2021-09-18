import numpy as np
from scipy.sparse import lil_matrix
import cv2


def create_sparse_matrix(points):
    matrix = lil_matrix(len(points),len(points))
    for row, column in enumerate(points):
        matrix[row,row] = 4
        border = [(column+1,column),(column-1,column),(column,column+1),(column,column-1)]
        for point in border:
            if point in points:
                index = points.index(point)
                matrix[row, index] = -1
    return matrix


def poisson_blend(source, target, mask):
    nonzero = np.nonzero(mask)
    points = zip(nonzero[0], nonzero[1])
    matrix = create_sparse_matrix(points)
    return 0
    


if __name__ == "__main__":
    source_name = input("Enter file name of source image ")
    target_name = input("Enter file name of target image ")
    mask_name = input("Enter file name of mask ")

    source_image = cv2.imread(source_name)
    target_image = cv2.imread(target_name)
    mask_image = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)

    mask = np.array(mask_image).astype(float)/255
    '''for i in range(len(mask)):
        if mask[i] != 1:
            mask[i] = 0'''
    mask[mask != 1] = 0
    mask = mask[:,:,0]
    RGBchannels = source_image.shape[-1]
    results = []
    for channel in range(RGBchannels):
        results.append(poisson_blend(source_image[:,:,channel], target_image[:,:,channel], mask))
    
    result = cv2.merge(results)

