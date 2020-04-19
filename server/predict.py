import os
import numpy as np
import cv2
from argparse import ArgumentParser
from keras.models import load_model
from keras.preprocessing.image import (
    img_to_array,
    load_img,
)
from model import createModel

# fetch image data as paramater
argParser = ArgumentParser()
argParser.add_argument(
    "-i", "--image", required=True, help="relative path to input image", type=str
)
args = vars(argParser.parse_args())

# declare constant variables
CWD = os.getcwd()
MODEL_WEIGHT_FILENAME = "DR_model_weights.h5"
PATH_TO_MODEL_WEIGHT = os.path.join(os.path.sep, CWD, MODEL_WEIGHT_FILENAME)
PATH_TO_INPUT_IMAGE = os.path.join(os.path.sep, CWD, args["image"])

WIDTH = 512
HEIGHT = 512
DEPTH = 3
inputShape = (HEIGHT, WIDTH, DEPTH)
NUM_OF_CLASSES = 2
# Initialize number of epochs to train for, initial learning rate and batch size
BS = 32


def convertIntToClass(i):
    switcher = {0: "No DR", 1: "DR"}
    return switcher.get(i, "Invalid class")


def convertImage(imageFullPath):
    loadedImage = load_img(imageFullPath)
    arr = img_to_array(loadedImage)
    arr = cv2.resize(arr, (HEIGHT, WIDTH))
    arr = np.array(arr, dtype="float")

    arr = arr.reshape(-1, HEIGHT, WIDTH, DEPTH)
    return arr


# load model
model = createModel(inputShape, NUM_OF_CLASSES)
model.load_weights(PATH_TO_MODEL_WEIGHT)


def predict(pathToInputImage):
    # convert image to np.array format
    print("INFO: converting image {}".format(pathToInputImage))
    arr = convertImage(pathToInputImage)

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
    return (predictionProbabilities, predictedLabel, predictedClass)


if __name__ == "__main__":
    predict(PATH_TO_INPUT_IMAGE)
