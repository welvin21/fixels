import pandas as pd
import numpy as np
import os
from argparse import ArgumentParser

argParser = ArgumentParser()
argParser.add_argument(
    "-l", "--labels", required=True, help="relative path to image labels in .csv format"
)
args = vars(argParser.parse_args())

CWD = os.getcwd()
LABELS_CSV = os.path.join(os.path.sep, CWD, args["labels"])


def fetchInconsistentData():
    hashTable, uniqueImageIDs = {}, set()
    df = pd.read_csv(LABELS_CSV)
    for index, row in df.iterrows():
        imageID, level = row["image"], row["level"]
        hashTable[imageID] = level
        uniqueImageIDs.add(imageID[: imageID.find("_")])

    f = open("../inconsistentIDs.txt", "w")
    for imageID in uniqueImageIDs:
        left = imageID + "_left"
        right = imageID + "_right"
        if hashTable[left] != hashTable[right]:
            f.write(imageID + "\n")
    f.close()


if __name__ == "__main__":
    fetchInconsistentData()
