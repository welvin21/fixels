from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.optimizers import Adam
from keras.metrics import Precision, Recall

# Initialize number of epochs to train for, initial learning rate and batch size
EPOCHS = 10
INIT_LR = 1e-4


def createModel(inputShape, numOfClasses):
    model = Sequential()
    model.add(Conv2D(32, (4, 4),
                            padding="valid",
                            strides=1,
                            input_shape=inputShape, activation="relu"))

    model.add(Conv2D(32, (4, 4), activation="relu"))

    model.add(Conv2D(32, (4, 4), activation="relu"))

    model.add(MaxPooling2D(pool_size=(8, 8)))

    model.add(Flatten())

    model.add(Dense(2048, activation="relu"))
    model.add(Dropout(0.25))

    model.add(Dense(2048, activation="relu"))
    model.add(Dropout(0.25))

    model.add(Dense(numOfClasses, activation="softmax"))

    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy",
                        optimizer=opt,
                        metrics=["accuracy", Precision(), Recall()])
    return model