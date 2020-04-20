import os
import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing.image import (
    img_to_array,
    load_img,
)
from model import createModel
from base64 import b64decode
from PIL import Image
from io import BytesIO

WIDTH = 512
HEIGHT = 512
DEPTH = 3

def convertIntToClass(i):
    switcher = {0: "No DR", 1: "DR"}
    return switcher.get(i, "Invalid class")


def resizeImageArray(arr):
    arr = cv2.resize(arr, (HEIGHT, WIDTH))
    arr = np.array(arr, dtype="float")
    arr = arr.reshape(-1, HEIGHT, WIDTH, DEPTH)
    return arr

def predict(model, imageBase64):
    imageBase64Decoded = b64decode(imageBase64)
    image = Image.open(BytesIO(imageBase64Decoded))
    arr = np.array(image)
    arr = resizeImageArray(arr)

    # predict the confidence values of each classes
    prediction = model.predict(arr)

    predictionProbabilities = prediction[0].tolist()
    # generate the actual class predicted
    predictedLabel = int(prediction.argmax(axis=-1)[0])
    predictedClass = convertIntToClass(predictedLabel)

    return (predictionProbabilities, predictedLabel, predictedClass)
