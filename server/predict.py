import os
import numpy as np
import cv2
from argparse import ArgumentParser
from keras.models import load_model
from keras.preprocessing.image import (
    img_to_array,
    load_img,
)

# fetch image data as paramater
argParser = ArgumentParser()
argParser.add_argument(
    "-i", "--image", required=True, help="relative path to input image", type=str
)
args = vars(argParser.parse_args())

# declare constant variables
CWD = os.getcwd()
MODEL_FILENAME = "DRModel.h5"
PATH_TO_MODEL = os.path.join(os.path.sep, CWD, MODEL_FILENAME)
PATH_TO_INPUT_IMAGE = os.path.join(os.path.sep, CWD, args["image"])

WIDTH = 128
HEIGHT = 128
DEPTH = 3
inputShape = (HEIGHT, WIDTH, DEPTH)

# Initialize number of epochs to train for, initial learning rate and batch size
BS = 100


def convertIntToClass(i):
    switcher = {0: "No DR", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "Proliferative"}
    return switcher.get(i, "Invalid class")


def convertImage(imageFullPath):
    loadedImage = load_img(imageFullPath)
    arr = img_to_array(loadedImage)
    arr = cv2.resize(arr, (HEIGHT, WIDTH))
    arr = np.array(arr, dtype="float")

    arr = arr.reshape(-1, HEIGHT, WIDTH, DEPTH)
    return arr


# convert image to np.array format
print("INFO: converting image {}".format(PATH_TO_INPUT_IMAGE))
arr = convertImage(PATH_TO_INPUT_IMAGE)

# load model
print("INFO: loading pre-trained model from {}\n".format(PATH_TO_MODEL))
model = load_model(PATH_TO_MODEL)
print("INFO: successfully loaded model from {}\n".format(PATH_TO_MODEL))
print("INFO: model: {}".format(model))

# predict the confidence values of each classes
print("INFO: predicting input image\n")
prediction = model.predict(arr)

print("INFO: prediction probability result :\n")
predictionProbabilities = prediction[0].tolist()
for i, probability in enumerate(predictionProbabilities):
    className = convertIntToClass(i)
    print("{}: {:0.4f}%".format(className, 100 * probability))

# generate the actual class predicted
predictedLabel = prediction.argmax(axis=-1)
predictedClass = convertIntToClass(predictedLabel[0])
print("\nINFO: predicted class result: {}".format(predictedClass))
