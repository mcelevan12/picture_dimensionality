import cPickle as pickle
import os
import csv
import random
from collections import defaultdict

def load_cats():
  cats_dir = "./cats"
  training_cats = {}
  test = []
  for condition in os.listdir(cats_dir):
    if os.path.isdir(os.path.join(cats_dir, condition)):
      if condition == "test":
        for picture_name in os.listdir(os.path.join(cats_dir, condition)):
          test.append(picture_name[:-4])
      else:
        training_cats[condition] = defaultdict(list)
        for cat in os.listdir(os.path.join(cats_dir, condition)):
          for picture_name in os.listdir(os.path.join(cats_dir, condition, cat)):
            training_cats[condition][cat].append(picture_name[:-4])
  return training_cats, test

def gen_training_data(condition, reduced_dict):
  training_data = []
  ctrl_flag = True
  for block in range(1,13):
    block_trials = []
    for cat in condition:
      outputs = [-1] * len(condition)
      outputs[list(condition.keys()).index(cat)] = 1
      for picture_name in condition[cat]:
        inputs = list(reduced_dict[picture_name])
        missing_dims = [0] * len(inputs)
        block_trials.append([int(ctrl_flag), block, picture_name] + inputs + outputs + missing_dims)
        ctrl_flag = False
    if training_data:
      random.shuffle(block_trials)
    training_data.extend(block_trials)
  return training_data

def header(col_key, cols):
  headers = []
  for i in range(1, cols + 1):
    headers.append(col_key + str(i))
  return headers

def save_traning_data(reduced_dict, training_cats, test, reduced_file):
  training_dir = "./training_data"
  csv_header = ["ctrl", "block", "picture_name"] + header("x", int(reduced_file[3:5])) + header("t", 2) + header("m", int(reduced_file[3:5]))
  for condition in training_cats:
    directory = os.path.join(training_dir, condition)
    if not os.path.exists(directory):
      os.makedirs(directory)
    with open(os.path.join(directory, reduced_file[:-4] + ".csv"), "w") as file:
      print("saving data for " + file.name)
      writer = csv.writer(file)
      writer.writerow(csv_header)
      for case in gen_training_data(training_cats[condition], reduced_dict):
        writer.writerow(case)


def load_PCA_data():
  data_dir = "./reduced_data/"
  training_cats, test = load_cats()
  for reduced_file in os.listdir(data_dir):
    with open(str(os.path.join(data_dir, reduced_file)), "r") as file:
      save_traning_data(pickle.load(file), training_cats, test, reduced_file)

load_PCA_data()
