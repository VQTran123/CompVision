import numpy as np
import scipy.sparse
import cv2

def matting(image, a1, a2):
    green_channel = np.atleast_2d(image[:,:,0])
    red_channel = np.atleast_2d(image[:,:,2])
    mat = np.copy(green_channel).astype(float)
    for i, k in enumerate(green_channel):
        mat[k] = 1 - a1*(green_channel[k] - a2*red_channel[k])
    return mat

if __name__ == "__main__":
    source_name = input("Enter file name of source image ")
    source_image = cv2.imread(source_name)
    source = np.atleast_3d(source_image).astype(float)
    mat = matting(source, 0.5, 1)
    cv2.imwrite("output.jpg", mat)