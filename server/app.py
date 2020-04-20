import os
from flask import Flask, request
from predict import predict
from model import createModel

WIDTH = 512
HEIGHT = 512
DEPTH = 3
INPUT_SHAPE = (HEIGHT, WIDTH, DEPTH)
NUM_OF_CLASSES = 2

CWD = os.getcwd()
PATH_TO_MODEL = os.path.join(os.path.sep, CWD, 'DR_model_weights_new.h5')
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

    return str(predict(model, imageBase64))


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
