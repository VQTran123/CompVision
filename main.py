import numpy as np
import scipy.sparse
import cv2

if __name__ == "__main__":
    source = input("Enter file name of source image")
    target = input("Enter file name of target image")
    mask = input("Enter file name of mask")

    source_image = cv2.imread(source)
    target_image = cv2.imread(target)
    mask_image = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
    