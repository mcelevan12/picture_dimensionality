#!/usr/bin python
import os
import csv
import numpy as np
from collections import defaultdict

def format_picture_col(picture_col):
  return picture_col.split()[3].split(".")[0]

def index_of_pictures(picture1, picture2):
  return picture1 + "," + picture2 if picture1 < picture2 else picture2 + "," + picture1

def read_data(file_name, data_points):
  file = open(file_name, "r")
  csv_reader = csv.reader(file, delimiter='\t')
  # remove junk header
  for _ in range(6):
    next(csv_reader)
  line_number = 0
  rating = -1;
  pictures = ["", ""]
  for row in csv_reader:
    if line_number % 3 == 2:
      while not row[9] == 'C':
        row = next(csv_reader)
      rating = int(row[7])
    else:
      pictures[line_number % 3] = format_picture_col(row[5])
    line_number+=1
    if line_number % 3 == 0:
      data_points[index_of_pictures(pictures[0], pictures[1])].append(rating)
  file.close()

def create_data_points():
  dataDir = "./distance_data/"
  data_points = defaultdict(list)
  for file_name in os.listdir(dataDir):
    if file_name.endswith(".txt"):
      read_data(os.path.join(dataDir, file_name), data_points)
  return data_points

def gen_distance_matrix():
  data_points = create_data_points()
  num_pictures = 48
  distance_matrix = [[0 for x in range(num_pictures)] for y in range(num_pictures)]
  low, high = 0, 0
  labels = []
  for picture_names in sorted(data_points):
    distance_matrix[high][low] = np.average(data_points[picture_names])
    distance_matrix[low][high] = np.average(data_points[picture_names])
    high += 1
    if high >= num_pictures:
      labels.append(picture_names.split(',')[0])
      low += 1
      high = low
  return distance_matrix, labels
