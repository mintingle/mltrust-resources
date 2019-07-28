import cv2
import csv
import os
import numpy as np

def create_img(img1_name, img2_name):
    img1= cv2.imread(img1_name)
    height1 = len(img1)
    width1 = len(img1[0])

    img2= cv2.imread(img2_name)
    height2 = len(img2)
    width2 = len(img2[0])


    #check which img is less wide and resize the other image to that width (downsample is prolly better than upsample here)
    if (width1 < width2):
        #resize img2 to img1
        scaleRatio = width1/width2
        newWidth = int(img2.shape[1] * scaleRatio)
        newHeight = int(img2.shape[0] * scaleRatio)
        dim = (newWidth, newHeight)
        resized = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
        img2 = resized
        height2 = len(img2)
        width2 = len(img2[0])
    else:
        #resize img1 to img2
        scaleRatio = width2/width1
        newWidth = int(img1.shape[1] * scaleRatio)
        newHeight = int(img1.shape[0] * scaleRatio)
        dim = (newWidth, newHeight)
        resized = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
        img1 = resized
        height1 = len(img1)
        width1 = len(img1[0])

    #make images the same height by adding bottom padding to smaller img
    if (height1 > height2):
        #add top and bottom padding to img2
        diff = height1-height2
        if(diff%2 == 0):
            paddingtop = int(diff/2)
            paddingbot = int(diff/2)
        else:
            diff = diff-1
            paddingtop = int(diff/2)
            paddingbot = int(diff/2 + 1)
        padded_pre_img = cv2.copyMakeBorder(img2, paddingtop, paddingbot, 0, 0, cv2.BORDER_CONSTANT, value=color)
        #padding = height1-height2 # for bottom only padding
        #padded_pre_img = cv2.copyMakeBorder(img2, 0, padding, 0, 0, cv2.BORDER_CONSTANT, value=color)
        img2 = padded_pre_img
        height2 = len(img2)
    else:
        #add top and bottom padding to img1
        diff = height2-height1
        if(diff%2 == 0):
            paddingtop = int(diff/2)
            paddingbot = int(diff/2)
        else:
            diff = diff-1
            paddingtop = int(diff/2)
            paddingbot = int(diff/2 + 1)
        padded_pre_img = cv2.copyMakeBorder(img1, paddingtop, paddingbot, 0, 0, cv2.BORDER_CONSTANT, value=color)
        #padding = height2-height1 # for bottom only padding
        #padded_pre_img = cv2.copyMakeBorder(img1, 0, padding, 0, 0, cv2.BORDER_CONSTANT, value=color)
        img1 = padded_pre_img
        height1 = len(img1)

    #add right padding (3% of width) to img1
    padding = round(width1*0.02)
    img1_rightpad = cv2.copyMakeBorder(img1, 0, 0, 0, padding, cv2.BORDER_CONSTANT, value=color)
    img1 = img1_rightpad

    #combine images
    combined = np.concatenate((img1, img2), axis=1)
    height = len(combined)
    width = len(combined[0])

    #scale to screen
    if(height > maxHeight):
        scaleRatio = maxHeight/height
        newWidth = int(combined.shape[1] * scaleRatio)
        newHeight = int(combined.shape[0] * scaleRatio)
        dim = (newWidth, newHeight)
        resized = cv2.resize(combined, dim, interpolation = cv2.INTER_AREA)
        combined = resized

        if(newWidth > maxWidth):
            padding = 0
        else:
            padding = round((maxWidth - newWidth)/2)
    else:
        if(newWidth > maxWidth):
            padding = 0
        else:
            padding = round((maxWidth - width)/2)

    #add right and left borders
    left, right = [padding]*2
    top, bottom = [0]*2

    img_with_border = cv2.copyMakeBorder(combined, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    cv2.imwrite('resized/'+img1_name[:-4]+' '+img2_name[:-4]+'.jpg', img_with_border)


color = [255,255, 255] #white border

maxWidth = 1300
maxHeight = 450

pairsList = []

#ShanghaiTech A incorrect
pairsList += [['IMG_46.jpg','IMG_81.jpg'], ['IMG_12.jpg', 'IMG_55.jpg'], ['IMG_26.jpg', 'IMG_65.jpg'], ['IMG_152.jpg', 'IMG_125.jpg']]

#ShanghaiTech A correct
pairsList += [['IMG_149.jpg', 'IMG_134.jpg'], ['IMG_57.jpg', 'IMG_164.jpg'], ['IMG_159.jpg', 'IMG_22.jpg'], ['IMG_47.jpg', 'IMG_157.jpg']]

#ShanghaiTech B incorrect
pairsList += [['IMG_16.jpg', 'IMG_290.jpg'], ['IMG_247.jpg', 'IMG_127.jpg'], ['IMG_267.jpg', 'IMG_130.jpg'], ['IMG_4.jpg', 'IMG_175.jpg']]

#ShanghaiTech B correct
pairsList += [['IMG_116.jpg', 'IMG_293.jpg'], ['IMG_139.jpg', 'IMG_275.jpg'], ['IMG_283.jpg', 'IMG_203.jpg'], ['IMG_228.jpg', 'IMG_215.jpg']]

#Venice incorrect
pairsList += [['b4901_001920.jpg', 'b4898_000960.jpg'], ['b4898_000840.jpg', 'a4896_004560.jpg'], ['b4901_000060.jpg', 'a4896_000840.jpg'], ['a4896_000120.jpg', 'b4895_001140.jpg']]

#Venice correct
pairsList += [['b4901_002160.jpg', 'b4898_000240.jpg'], ['b4895_001680.jpg', 'a4896_004740.jpg'], ['a4896_000720.jpg', 'b4901_001140.jpg'], ['b4895_000180.jpg', 'b4895_000720.jpg']]

#QNRF incorrect
pairsList += [['img_0885.jpg', 'img_1188.jpg'], ['img_0797.jpg', 'img_0217.jpg'], ['img_0013.jpg', 'img_0614.jpg'], ['img_0027.jpg', 'img_0921.jpg']]

#QNRF correct
pairsList += [['img_0901.jpg', 'img_1056.jpg'], ['img_0427.jpg', 'img_1151.jpg'], ['img_0932.jpg', 'img_0244.jpg'], ['img_0457.jpg', 'img_1000.jpg']]

#EXTRAS
pairsList += [['img_0999.jpg', 'img_0876.jpg']]

for pair in pairsList:
    create_img(pair[0], pair[1])