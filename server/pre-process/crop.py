import os
import cv2
import numpy as np
from argparse import ArgumentParser

argParser = ArgumentParser()
argParser.add_argument('-s', '--size', default=256, help='new image size after cropping and resizing', type=int)
argParser.add_argument('-f', '--folder', required=True, help='relative path to directory containing images to be cropped', type=str)

args = vars(argParser.parse_args())

NEW_IMAGE_SIZE = args['size']
RELATIVE_PATH_TO_FOLDER = args['folder'].strip('/')
NEW_FOLDER_NAME = RELATIVE_PATH_TO_FOLDER + '-cropped'

def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def cropAndResizeImages(path, newPath, imgSize):
    path += '/'
    newPath += '/'
    
    createDirectory(newPath)
    dirs = [image for image in os.listdir(path) if image != '.DS_Store']
    total = 0

    for item in dirs:
        total += 1

        imgGrayscale = cv2.imread(path + item, cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(path+item)
        tolerance = 10
        mask = imgGrayscale > tolerance     

        img = img[np.ix_(mask.any(1),mask.any(0))]
        cv2.imwrite(newPath + item, img)

        print("Saving: ", item, total)


if __name__ == '__main__':
    cropAndResizeImages(path=RELATIVE_PATH_TO_FOLDER, newPath=NEW_FOLDER_NAME, imgSize=NEW_IMAGE_SIZE)
