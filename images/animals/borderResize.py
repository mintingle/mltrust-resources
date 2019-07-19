import cv2
import csv
import os

color = [255,255, 255] #white border

top, bottom = [0]*2
maxWidth = 1300
maxHeight = 450

filesList = os.listdir('.')
filesList.sort()

for filename in filesList:
    if(filename[-5:] == '.JPEG'):
        img = cv2.imread(filename)
        height = len(img)
        width = len(img[0])

        padding = 100

        if(height > maxHeight):
            scaleRatio = maxHeight/height
            newWidth = int(img.shape[1] * scaleRatio)
            newHeight = int(img.shape[0] * scaleRatio)
            dim = (newWidth, newHeight)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            img = resized

            padding = int((maxWidth - newWidth)/2)
        else:
            padding = int((maxWidth - width)/2)          

        left, right = [padding]*2

        img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        cv2.imwrite('resized/'+filename, img_with_border)
