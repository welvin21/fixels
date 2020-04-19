import numpy as np
import pandas as pd
import os
import random
import sys
import cv2
import time
import csv
from argparse import ArgumentParser
from subprocess import check_output
from matplotlib import pyplot as plt
from keras.preprocessing.image import (
    ImageDataGenerator,
    array_to_img,
    img_to_array,
    load_img,
)
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical, print_summary
from keras.callbacks import EarlyStopping
from model import createModel

# Fetch training param from argparse
argParser = ArgumentParser()
argParser.add_argument(
    "-t", "--train-size", default=1000, help="Training data size", type=int
)
argParser.add_argument(
    "-f",
    "--folder",
    required=True,
    help="Relative path of the training dataset",
    type=str,
)
argParser.add_argument(
    "-l",
    "--labels",
    required=True,
    help="Relative path of predicted value (labels) in .csv format",
    type=str,
)
args = vars(argParser.parse_args())

# Declare constant variables
CWD = os.getcwd()
TRAIN_DATASETS_PATH = os.path.join(os.path.sep, CWD, args["folder"])
TRAIN_LABELS_PATH = os.path.join(os.path.sep, CWD, args["labels"])
TRAIN_DATA_SIZE = args["train_size"]
TEST_DATA_SIZE = 0.2

NUM_OF_CLASSES = 5
WIDTH = 512
HEIGHT = 512
DEPTH = 3
inputShape = (HEIGHT, WIDTH, DEPTH)

# Initialize number of epochs to train for, initial learning rate and batch size
EPOCHS = 10
INIT_LR = 1e-4
BS = 32

ImageNameDataHash = {}
uniquePatientIDList = []

def removeExt(filename):
    exts = ['.jpg', '.png', '.jpeg']
    for ext in exts:
        filename = filename.replace(ext, '')
        filename = filename.replace(ext.upper(), '')
    return filename

def getTrainData(trainDir, numberOfTrainData=1000):
    global ImageNameDataHash
    startTime = time.time()

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
        ImageNameDataHash[removeExt(image)] = np.array(arr)

        if len(ImageNameDataHash) % 100 == 0:
            print("INFO: Successfully loaded {} images".format(len(ImageNameDataHash)))

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
    return rawDF


def reshapeData(dataframe):
    output = np.zeros([dataframe.shape[0], HEIGHT, WIDTH, DEPTH])
    for i in range(dataframe.shape[0]):
        output[i] = dataframe[i]
    return output


getTrainData(TRAIN_DATASETS_PATH, TRAIN_DATA_SIZE)
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
uniqueIDs = mainDF.image.unique()
trainIDs, testIDs = train_test_split(
    uniqueIDs, test_size=TEST_DATA_SIZE, random_state=10
)

print("INFO: train-test split is successfully done\n")
print("INFO: train data size: {}\n".format(len(trainIDs.tolist())))
print("INFO: test data size: {}\n".format(len(testIDs.tolist())))

# Further processing of train and test data
train = mainDF[mainDF.image.isin(trainIDs.tolist())]
test = mainDF[~mainDF.image.isin(trainIDs.tolist())]

train = train.reset_index(drop=True)
test = test.reset_index(drop=True)

trainX, trainY = train["data"], train["level"]
testX, testY = test["data"], test["level"]

trainY = to_categorical(trainY, num_classes=NUM_OF_CLASSES)
testY = to_categorical(testY, num_classes=NUM_OF_CLASSES)

# reshape data before training process
trainX = reshapeData(trainX)
testX = reshapeData(testX)

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

# initialize model
print("INFO: compiling cnn model\n")
model = createModel(inputShape, NUM_OF_CLASSES)
print("INFO: model is ready : {}\n".format(model))
print("INFO: model summary")
print_summary(model, line_length=None, positions=None, print_fn=None)

# train the network
print("INFO: training previously created cnn model")
sys.stdout.flush()

stop = EarlyStopping(monitor="val_accuracy", min_delta=0.001, patience=3, mode="auto")

history = model.fit(
    aug.flow(trainX, trainY, batch_size=BS),
    validation_data=(testX, testY),
    steps_per_epoch=len(trainX) // BS,
    epochs=EPOCHS,
    verbose=1,
    callbacks=[stop]
)
loss, acc = model.evaluate(testX, testY, verbose=1)
print("\nINFO: Original model, accuracy: {:5.2f}%\n".format(acc * 100))

# save model to local machine
print("INFO: saving model to disk")
sys.stdout.flush()
model.reset_metrics()
model.save("./DRmodel.h5")
