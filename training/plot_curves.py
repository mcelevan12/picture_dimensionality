import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import data

def save_fig(scores):
  trials = range(1, 13)
  plt.rcParams.update({'font.size': 20})
  plt.rcParams["figure.figsize"] = [12.8, 9.6]
  for condition in scores:
    plt.plot(trials, np.mean(scores[condition], axis = 0), label = condition)
  plt.legend()
  plt.show()
  plt.savefig('learning_curves.png')

def main():
  save_fig(data.avg_data())

main()
