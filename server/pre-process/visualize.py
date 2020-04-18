import pandas as pd
import numpy as np
import os
from argparse import ArgumentParser
from matplotlib import pyplot as plt

argParser = ArgumentParser()
argParser.add_argument('-l', '--labels', required=True, help='relative path to image labels in .csv format')
args = vars(argParser.parse_args())

CWD = os.getcwd()
LABELS_CSV = os.path.join(os.path.sep, CWD, args['labels'])

def visualize():
  df = pd.read_csv(LABELS_CSV)
  df = df.values.tolist()

  data = [value for (imageID, value) in df]
  labels = np.unique(data).tolist()
  counts = []

  for label in labels:
    counts.append(data.count(label))

  print(counts)
  plt.bar(labels, counts, align='center')
  plt.show()

if __name__ == '__main__':
  visualize()