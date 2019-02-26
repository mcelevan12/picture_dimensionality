import os
import matplotlib.pyplot as plt
import numpy as np
import csv

def import_scores(file_name, scores, condition):
  file = open(file_name, "r")
  csv_reader = csv.reader(file, delimiter='\t')
  # remove junk header
  for _ in range(6):
    next(csv_reader)
  line_number = 0;
  correct = [0]
  for row in csv_reader:
    line_number += 1
    while row[6] == "Ok":
      row = next(csv_reader)
    if row[6] == row[13]:
      correct[-1] += 1
    if line_number%(18*12) == 0:
      correct[-1] /= 18.0
      break
    if line_number%18 == 0:
      correct[-1] /= 18.0
      correct.append(0)
  if line_number%(12*18) != 0:
    print(file_name + " is short")
  else:
    scores.setdefault(condition, []).append(correct)

def raw_data():
  scores = {}
  dataDir = "./human_responses/"
  for file_name in os.listdir(dataDir):
    if file_name.endswith(".txt"):
      import_scores(os.path.join(dataDir, file_name), scores, file_name[0])
  return scores

def avg_data():
  scores = raw_data()
  avg_scores = {}
  for condition in scores.keys():
    avg_scores[condition] = np.mean(np.array(scores[condition]), axis=0)
  return avg_scores

print(avg_data())
