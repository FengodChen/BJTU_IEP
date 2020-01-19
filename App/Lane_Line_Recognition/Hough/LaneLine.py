import cv2 as cv
import numpy as np
import sys

#hsv_lower = np.array([0, 0, 180])
#hsv_upper = np.array([161, 19, 225])
hsv_lower = np.array([0, 0, 220])
hsv_upper = np.array([255, 255, 255])

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

def BGR2HSV(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    return img_hsv

def equalHSV(hsv_img):
    (h, s, v) = cv.split(hsv_img)
    h = cv.equalizeHist(h)
    s = cv.equalizeHist(s)
    v = cv.equalizeHist(v)
    hsv_img_eq = cv.merge((h, s, v))
    return hsv_img_eq

def binaryLaneLine(bgr_img):
    bgr_img = cv.GaussianBlur(bgr_img, (5, 5), 3)
    hsv_img = BGR2HSV(bgr_img)
    #hsv_lower = np.array([0, 0, 120])
    #hsv_upper = np.array([120, 90, 250])
    binary_img = cv.inRange(hsv_img, hsv_lower, hsv_upper)
    binary_img = cv.erode(binary_img, (3, 3))
    binary_img = cv.dilate(binary_img, (3, 3))
    return binary_img

def binaryLaneLine_callback(arg):
    #bgr_img = arg[0]
    #windowsName = arg[1]
    bgr_img = img
    windowsName = imgPath
    bgr_img = cv.GaussianBlur(bgr_img, (5, 5), 3)
    hsv_img = BGR2HSV(bgr_img)
    hsv_img = equalHSV(hsv_img)
    hsv_lower = np.array([cv.getTrackbarPos('H_MIN', windowsName), cv.getTrackbarPos('S_MIN', windowsName), cv.getTrackbarPos('V_MIN', windowsName)], 'int')
    hsv_upper = np.array([cv.getTrackbarPos('H_MAX', windowsName), cv.getTrackbarPos('S_MAX', windowsName), cv.getTrackbarPos('V_MAX', windowsName)], 'int')
    #print("hsv_lower={}, hsv_upper={}".format(hsv_lower, hsv_upper))
    binary_img = cv.inRange(hsv_img, hsv_lower, hsv_upper)
    binary_img = cv.erode(binary_img, (3, 3))
    binary_img = cv.dilate(binary_img, (3, 3))
    cv.imshow(windowsName, binary_img)

def showImg_GUI(img, imgPath):
    cv.namedWindow(imgPath, cv.WINDOW_NORMAL)
    cv.resizeWindow(imgPath, 640, 480)
    cv.imshow(imgPath, img)
    h_min_range = h_max_range = 255
    s_min_range = s_max_range = 255
    v_min_range = v_max_range = 255
    h_min_init = hsv_lower[0]
    h_max_init = hsv_upper[0]
    s_min_init = hsv_lower[1]
    s_max_init = hsv_upper[1]
    v_min_init = hsv_lower[2]
    v_max_init = hsv_upper[2]
    cv.createTrackbar('H_MIN', imgPath, h_min_init, h_min_range, binaryLaneLine_callback)
    cv.createTrackbar('H_MAX', imgPath, h_max_init, h_max_range, binaryLaneLine_callback)
    cv.createTrackbar('S_MIN', imgPath, s_min_init, s_min_range, binaryLaneLine_callback)
    cv.createTrackbar('S_MAX', imgPath, s_max_init, s_max_range, binaryLaneLine_callback)
    cv.createTrackbar('V_MIN', imgPath, v_min_init, v_min_range, binaryLaneLine_callback)
    cv.createTrackbar('V_MAX', imgPath, v_max_init, v_max_range, binaryLaneLine_callback)
    #binaryLaneLine_callback((img, imgPath))
    binaryLaneLine_callback(0)
    cv.waitKey(0)
    cv.destroyAllWindows()

def houghLaneLine(img, binary_img):
    lines = cv.HoughLines(binary_img, 1.0, np.pi / 200, 120)
    
    for [[r,theta]] in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv.line(img,(x1,y1), (x2,y2), (0,0,255),2)
    '''
    lines = cv.HoughLinesP(binary_img,1,np.pi/180,100,10,100)
    for [[x1,y1,x2,y2]] in lines:
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    '''
    return img

def showImg(img, imgPath):
    cv.namedWindow(imgPath, cv.WINDOW_NORMAL)
    cv.resizeWindow(imgPath, 640, 480)
    cv.imshow(imgPath, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    imgPath = 'no_car.jpg'
    if (sys.argv[1]):
        imgPath = sys.argv[1]
    img = openImg(imgPath, (0, 1, 0.3, 1))
    #img = openImg(imgPath)
    # Trackbar
    img = cv.GaussianBlur(img, (5, 5), 3)
    showImg_GUI(img, imgPath)
    # Hough
    #bin_img = binaryLaneLine(img)
    #img = houghLaneLine(img, bin_img)
    # HSV
    #img = cv.GaussianBlur(img, (5, 5), 3)
    #img = BGR2HSV(img)
    #showImg(img, imgPath)