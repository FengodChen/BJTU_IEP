import cv2 as cv

def openImg(imgPath, scope = (0.0, 1.0, 0.0, 1.0)):
    ''' Open Image with path and scope

    imgPath:    
        Type: string
        Mean: Path of image.

    scope:
        Type: float 
        Mean: (yMin, yMax, xMin, xMax), range from 0.0 to 1.0.
    '''
    img = cv.imread(imgPath)
    (ySum, xSum, dim) = img.shape
    img = img[
              int(ySum*scope[0]): int(ySum*scope[1]),
              int(xSum*scope[2]): int(xSum*scope[3])
              ]
    return img

if __name__ == "__main__":
    img = openImg('test.jpg', (0.0, 0.5, 0.0, 0.5))
    cv.imshow('test', img)
    cv.waitKey(0)