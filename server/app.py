import os
import json
from argparse import ArgumentParser
from flask import Flask, request
from predict import predict
from model import createModel

argsParser = ArgumentParser()
argsParser.add_argument('-m', '--model', required=True, help='path to model weights in .h5 format')
args = vars(argsParser.parse_args())

WIDTH = 512
HEIGHT = 512
DEPTH = 3
INPUT_SHAPE = (HEIGHT, WIDTH, DEPTH)
NUM_OF_CLASSES = 2

CWD = os.getcwd()
PATH_TO_MODEL = os.path.join(os.path.sep, CWD, args['model'])
model = createModel(INPUT_SHAPE, NUM_OF_CLASSES)
model.load_weights(PATH_TO_MODEL)

app = Flask(__name__)

@app.route("/")
def sample():
    return "ok"

@app.route("/predict", methods=["POST"])
def main():
    req = request.get_json()
    imageBase64 = req['imageBase64'] 

    probabilities, predictedLabel, predictedClass = predict(model, imageBase64)
    
    prediction = {}
    prediction['probabilities'] = {"NoDR": probabilities[0], "DR": probabilities[1]}
    prediction['label'] = predictedLabel
    prediction['class'] = predictedClass
    
    print()
    print(prediction)
    return json.dumps(prediction)


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
