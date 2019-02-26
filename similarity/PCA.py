import data
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import os
import pickle

def picture_name(label):
  return label[:-4]

def categories(labels):
  cats = np.full(len(labels), -1)
  for file_name in os.listdir("./"):
    if "cat" in file_name:
      for label in os.listdir(os.path.join("./", file_name)):
        cats[labels.index(picture_name(label))] = int(file_name[-1])
  return cats

def print_data_loss():
  distance_matrix, labels = data.gen_distance_matrix()
  sklearn_pca = sklearnPCA(n_components=48)
  std_distance_matrix = StandardScaler().fit_transform(distance_matrix)
  sklearn_pca.fit(std_distance_matrix)
  row = 1
  sum = 0
  for ratio in sklearn_pca.explained_variance_ratio_:
    print(str(row) + ":\t" + str(round(ratio * 100, 2)) + ",\t" + str(round(sum + ratio * 100, 2)))
    row += 1
    sum += ratio * 100

def main():
  distance_matrix, labels = data.gen_distance_matrix()
  for i in range(1, 13):
    sklearn_pca = sklearnPCA(n_components=i)
    std_distance_matrix = StandardScaler().fit_transform(distance_matrix)
    reduced_data = sklearn_pca.fit_transform(std_distance_matrix)
    with open('../training/reduced_data/PCA' + "{:02d}".format(i) + ".txt", 'wb') as file:
      pickle.dump(dict(zip(labels, reduced_data)), file)

main()
