import numpy as np
import scipy.sparse
import cv2

def matting(image, a1, a2):
    green_channel = np.atleast_2d(image[:,:,1]).astype(float)/255
    red_channel = np.atleast_2d(image[:,:,0]).astype(float)/255
    print(green_channel)
    mat = 1.0 - a1*(green_channel - green_channel*a2)
    print(mat)
    mat = mat*255
    return mat

if __name__ == "__main__":
    #source_name = input("Enter file name of source image ")
    source_name = "testing_1.png"
    source_image = cv2.imread(source_name)
    source = np.atleast_3d(source_image).astype(float)
    mat = matting(source, 1.0, 0.01)
    cv2.imwrite("output.png", mat)