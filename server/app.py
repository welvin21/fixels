import os
import json
from argparse import ArgumentParser
from flask import Flask, request
from flask_cors import CORS, cross_origin
from predict import Predictor
from model import Model

argsParser = ArgumentParser()
argsParser.add_argument(
    "-m", "--model", required=True, help="path to model weights in .h5 format"
)
args = vars(argsParser.parse_args())

INPUT_SHAPE = (512, 512, 3)
NUM_OF_CLASSES = 2

CWD = os.getcwd()
PATH_TO_MODEL = os.path.join(os.path.sep, CWD, args["model"])
modelInstance = Model(INPUT_SHAPE, NUM_OF_CLASSES)
model = modelInstance.createModel()
model.load_weights(PATH_TO_MODEL)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def sample():
    return "ok"


@app.route("/predict", methods=["POST"])
@cross_origin()
def main():
    req = request.get_json()
    imageBase64 = req["imageBase64"]

    predictorInstance = Predictor(model, imageBase64)
    probabilities, predictedLabel, predictedClass = predictorInstance.predict()

    prediction = {}
    prediction["probabilities"] = {"NoDR": probabilities[0], "DR": probabilities[1]}
    prediction["label"] = predictedLabel
    prediction["class"] = predictedClass

    print()
    print(prediction)
    return json.dumps(prediction)


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
