import numpy as np
import scipy.sparse
import cv2
import composite

def matting(image, a1, a2):
    green_channel = np.atleast_2d(image[:,:,1]).astype(float)/255
    red_channel = np.atleast_2d(image[:,:,0]).astype(float)/255
    mat = 1.0 - a1*(green_channel - red_channel*a2)
    #print(mat)
    mat[mat < 0.8] = 0
    '''nonzeros = np.nonzero(mat)
    points = list(zip(nonzeros[0],nonzeros[1]))
    for p in points:
        print(mat[p])'''
    mat[mat > 0] = 1
    #print(mat)
    mat = mat*255
    return mat

if __name__ == "__main__":
    #source_name = input("Enter file name of source image ")
    #source_name = "testing_1.png"
    target_name = "howl.jpg"
    source_name = "radke.mp4"
    #source_name = "green.jpg"
    if source_name[len(source_name)-4:] == ".png" or source_name[len(source_name)-4:] == ".jpg":
        source_image = cv2.imread(source_name)
        target_image = cv2.imread(target_name)
        target = np.atleast_3d(target_image).astype(float)
        source = np.atleast_3d(source_image).astype(float)
        mat = matting(source, 1, 1)
        cv2.imwrite("mat_output.jpg", mat)
        results = []
        for channel in range(3):
            results.append(composite.poisson_blend(source[:,:,channel], target[:,:,channel], mat))
        result = cv2.merge(results)
        cv2.imwrite("output.jpg", result)
    else:
        #source_video = cv2.VideoCapture(source_name)
        img_array = []
        for i in range(1,173):
            img = cv2.imread("output_" + str(i) + ".jpg")
            height, width, layers = img.shape
            img_array.append(img)
        out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (width, height))
        target_image = cv2.imread(target_name)
        target = np.atleast_3d(target_image).astype(float)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release
        '''
        while(source_video.isOpened()):
            i += 1
            ret, frame = source_video.read()
            if ret == True:
                source = np.atleast_3d(frame).astype(float)
                mat = matting(source, 1, 1)
                results = []
                for channel in range(3):
                    results.append(composite.poisson_blend(source[:,:,channel], target[:,:,channel], mat))
                result = cv2.merge(results)
                cv2.imwrite("output_" + str(i) + ".jpg", result)
                #out.write(result)
                #cv2.imshow("frame",result)
                #if cv2.waitKey(5) and 0xFF == ord('q'):
                #    break
            else:
                break
        source_video.release()
        '''
        #out.release()
        

    