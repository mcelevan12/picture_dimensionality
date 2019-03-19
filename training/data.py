from collections import defaultdict
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import mean

def pic_name(row):
  return row[5].split(' ')[2][:-5]

def import_final_test(file_name, results):
  csv_reader = csv.reader(open(file_name, 'r'), delimiter='\t')
  row = next(csv_reader)
  #hate this:(
  while "Test" not in (row + [""]*5)[4]:
    row = next(csv_reader)
  #go to final block
  results[pic_name(row)].append("Cumby" in row[6] )
  for row in csv_reader:
    results[pic_name(row)].append("Cumby" in row[6])

def import_scores_per_pic(file_name, scores):
  csv_reader = csv.reader(open(file_name, "r"), delimiter='\t')
  row = next(csv_reader)
  while "Training" not in (row + [""]*5)[3]:
    row = next(csv_reader)
  while "Training" in row[3]:
    while row[6] == "Ok":
      row = next(csv_reader)
    scores[pic_name(row)].append(row[6] == row[13])
    row = next(csv_reader)

def import_avg_scores(file_name, scores, condition):
  file = open(file_name, "r")
  csv_reader = csv.reader(file, delimiter='\t')
  # remove junk header
  for _ in range(7):
    row = next(csv_reader)
  line_number = 0;
  correct = [0]
  while "Training" in row[3]:
    while row[6] == "Ok":
      row = next(csv_reader)
    if row[6] == row[13]:
      correct[-1] += 1
    row = next(csv_reader)
    line_number += 1
    if line_number%18 == 0:
      correct[-1] /= 18.0
      if "Training" in row[3]:
        correct.append(0)
  if line_number < 12*18:
    print(file_name + " is short")
    print(line_number)
  else:
    scores.setdefault(condition, []).append(correct)

def avg_test_data():
  dir = "./human_responses/"
  results = {}
  results["N"] = defaultdict(list)
  results["F"] = defaultdict(list)
  results["R"] = defaultdict(list)
  for file_name in os.listdir(dir):
    import_final_test(os.path.join(dir, file_name), results[file_name[0:1]])
  for condition in results:
    print(condition)
    for picture_name in results[condition]:
      print(picture_name + ": " + str(mean(results[condition][picture_name])))

avg_test_data()

def avg_block_data():
  scores = {}
  dataDir = "./human_responses/"
  for file_name in os.listdir(dataDir):
    if file_name.endswith(".txt"):
      import_avg_scores(os.path.join(dataDir, file_name), scores, file_name[0])
  avg_block_scores = {}
  for condition in scores.keys():
    avg_block_scores[condition] = np.mean(np.array(scores[condition]), axis=0)
  return avg_block_scores
