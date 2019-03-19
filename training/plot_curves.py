import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import data

def plot_learning_curves(scores):
  trials = range(1, 13)
  plt.rcParams.update({'font.size': 20})
  plt.rcParams["figure.figsize"] = [12.8, 9.6]
  for condition in scores:
    plt.plot(trials, scores[condition], label = condition)
  plt.legend()
  plt.show()
  plt.savefig('./learning_curves.png')

#plot_learning_curves(data.avg_block_data())
plot

