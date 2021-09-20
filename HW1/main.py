import numpy as np
import scipy.sparse
import cv2

if __name__ == "__main__":
    source = input("dog.png")
    target = input("beach.png")
    mask = input("mask1.png")
    
    source_image = cv2.imread("dog.png")
    target_image = cv2.imread(target)
    mask_image = cv2.imread("mask1.png", cv2.IMREAD_GRAYSCALE)

    print(len(source_image[0]))
    #print(target_image[0])
    source_image = cv2.imwrite("dog.png",mask_image[0])
