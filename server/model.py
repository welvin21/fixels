import numpy as np
import pandas as pd
import os
import random
import sys
import cv2
import time
import csv
from subprocess import check_output

from matplotlib import pyplot as plt
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
CWD = os.getcwd()
TRAIN_DATASETS_PATH = os.path.join(os.path.sep, CWD, "datasets/train")
TRAIN_LABELS_PATH = os.path.join(os.path.sep, CWD, "datasets/trainLabels.csv")
TEST_DATA_SIZE = 0.2

NUM_OF_CLASSES = 5
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


def getTrainData(trainDir, numberOfTrainData=1000):
    global ImageNameDataHash
    startTime = time.time()
    if numberOfTrainData > 35126:
        print("ERROR: max number of train data exceeded\n")
        return

    images = os.listdir(trainDir)
    print(
        "INFO: Number of images found in {}: {} images.\n".format(trainDir, len(images))
    )
    print(
        "INFO: Fetching {} sample images from training datasets\n".format(
            numberOfTrainData
        )
    )
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

        if len(ImageNameDataHash) == numberOfTrainData:
            break
    print(
        "INFO: Successfully loaded {} images within {} seconds\n".format(
            numberOfTrainData, time.time() - startTime
        )
    )
    return


def getTrainLabels(fileLocation):
    rawDF = pd.read_csv(fileLocation)
    numOfRows, numOfColumns = rawDF.shape[0], rawDF.shape[1]
    print(
        "INFO: fetching train labels csv, found {} rows and {} columns of data\n".format(
            numOfRows, numOfColumns
        )
    )

    # Double check if left and right data of a particular patient are the same
    rawDF["PatientID"] = ""
    ImageLevelHash = {}
    patientIDList = set()
    for index, row in rawDF.iterrows():
        key = row[0] + ""
        patientID = row[0] + ""
        patientID = patientID.replace("_right", "")
        patientID = patientID.replace("_left", "")
        rawDF.at[index, "PatientID"] = patientID
        patientIDList.add(patientID)
        ImageLevelHash[key] = str(row[1])

    inconsistentDataCount = 0
    for patientID in patientIDList:
        leftLevel = ImageLevelHash["{}_left".format(patientID)]
        rightLevel = ImageLevelHash["{}_right".format(patientID)]

        if leftLevel != rightLevel:
            inconsistentDataCount += 1
            print(
                "WARNING: patient {}'s data are not consistent. left -> {}. right -> {}".format(
                    patientID, leftLevel, rightLevel
                )
            )
    print()
    print("INFO: number of inconsistent data: {}".format(inconsistentDataCount))
    print("INFO: number of unique patients: {}\n".format(len(patientIDList)))
    return rawDF


getTrainData(TRAIN_DATASETS_PATH, 20)
trainLabelsDF = getTrainLabels(TRAIN_LABELS_PATH)

keepImages = list(ImageNameDataHash.keys())
trainLabelsDF = trainLabelsDF[trainLabelsDF["image"].isin(keepImages)]

# Combine train image labels and data to one dataframe
imageName, imageData = [], []
for index, row in trainLabelsDF.iterrows():
    key = str(row[0])
    if key in ImageNameDataHash:
        value = ImageNameDataHash[key]
        imageName.append(key)
        imageData.append(np.array(value))

mainDF = pd.DataFrame({"image": imageName, "data": imageData})

# trainLabelsDF and mainDF have to be in the same length
if trainLabelsDF.shape[0] != mainDF.shape[0]:
    print(
        "ERROR: trainLabelsDF (length: {}) is not the same length as mainDF (length: {})".format(
            trainLabelsDF.shape[0], mainDF.shape[0]
        )
    )

# Merge trainLabelsDF to mainDF
mainDF = pd.merge(trainLabelsDF, mainDF, left_on="image", right_on="image", how="outer")

# Split data into train and test data
print(
    "INFO: splitting dataset into train and test (test size : {}%)\n".format(
        TEST_DATA_SIZE * 100
    )
)
sys.stdout.flush()
uniqueIDs = mainDF.PatientID.unique()
trainIDs, testIDs = train_test_split(
    uniqueIDs, test_size=TEST_DATA_SIZE, random_state=10
)

print("INFO: train-test split is successfully done\n")
print("INFO: train data size: {}\n".format(len(trainIDs.tolist())))
print("INFO: test data size: {}\n".format(len(testIDs.tolist())))

# Further processing of train and test data
train = mainDF[mainDF.PatientID.isin(trainIDs.tolist())]
test = mainDF[~mainDF.PatientID.isin(trainIDs.tolist())]

train = train.reset_index(drop=True)
test = test.reset_index(drop=True)

trainX, trainY = train["data"], train["level"]
testX, testY = test["data"], test["level"]

trainY = to_categorical(trainY, num_classes=NUM_OFCLASSES)
testY = to_categorical(testY, num_classes=NUM_OF_CLASSES)

# construct the image generator for data augmentation
sys.stdout.flush()
aug = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)
