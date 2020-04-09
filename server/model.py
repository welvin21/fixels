import numpy as np
import pandas as pd
import os
import random
import sys
import cv2
import time
import matplotlib
from subprocess import check_output

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.preprocessing.image import (
    ImageDataGenerator,
    array_to_img,
    img_to_array,
    load_img,
)
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

# Declare constant variables
TRAIN_DATASETS_PATH = os.path.join(os.path.sep, os.getcwd(), "datasets/train")
NUM_CLASSES = 5
WIDTH = 128
HEIGHT = 128
DEPTH = 3
inputShape = (HEIGHT, WIDTH, DEPTH)

# Initialize number of epochs to train for, initial learning rate and batch size
EPOCHS = 15
INIT_LR = 1e-3
BS = 32

ImageNameDataHash = {}
uniquePatientIDList = []


def convertIntToClass(i):
    switcher = {0: "No DR", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "Proliferative"}
    return switcher.get(i, "Invalid class")


def convertClassToInt(label):
    label = label.strip()
    switcher = {"No DR": 0, "Mild": 1, "Moderate": 2, "Severe": 3, "Proliferative": 4}
    return switcher.get(label, "Invalid class")


def getTrainData(trainDir, numberOfTrainData = 1000):
    startTime = time.time()
    if(numberOfTrainData > 35126):
        print('ERROR: max number of train data exceeded')
        return
    
    global ImageNameDataHash
    images = os.listdir(trainDir)
    print("Number of images found in {}: {} images.".format(trainDir, len(images)))
    print("Fetching {} sample images from training datasets".format(numberOfTrainData))
    for image in images:
        imageFullPath = os.path.join(os.path.sep, trainDir, image)
        loadedImage = load_img(imageFullPath)
        arr = img_to_array(loadedImage)

        dim1, dim2, dim3 = arr.shape[0], arr.shape[1], arr.shape[2]
        if dim1 < HEIGHT or dim2 < WIDTH or dim3 < DEPTH:
            print("ERROR: dimensions of {} are less than expected.".format(image))

        # Resize image dimensions
        arr = cv2.resize(arr, (HEIGHT, WIDTH))

        dim1, dim2, dim3 = arr.shape[0], arr.shape[1], arr.shape[2]
        if dim1 != HEIGHT or dim2 != WIDTH or dim3 != DEPTH:
            print(
                "ERROR: image resizing failed, dimensions of {} are not the same as expected -> {}.".format(
                    image, inputShape
                )
            )

        # Store np.array version of image to ImageNameDataHash
        arr = np.array(arr, dtype="float")
        ImageNameDataHash[image.replace(".jpeg", "")] = np.array(arr)

        if(len(ImageNameDataHash) == numberOfTrainData):
            break
    print('Successfully loaded {} images within {} seconds'.format(numberOfTrainData, time.time() - startTime))
    return


getTrainData(TRAIN_DATASETS_PATH, 200)
