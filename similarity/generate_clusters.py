import data
import os
import matplotlib.pyplot as plt
import heapq
import Queue as Q
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from scipy.spatial.distance import pdist
from shutil import copyfile, rmtree

def create_category(linkage_matrix, root, labels, src, dest):
  q = Q.Queue()
  q.put(root)
  while not q.empty():
    current = q.get()
    if current.is_leaf():
      copyfile(
        os.path.join(src, labels[current.id] + ".jpg"),
        os.path.join(dest, labels[current.id] + ".jpg")
      )
    else:
      q.put(current.left)
      q.put(current.right)

def main():
  distance_matrix, labels = data.gen_distance_matrix()
  np.save('../labels', labels)
  linkage_matrix = linkage(distance_matrix, 'ward')
  plt.figure(figsize=(25, 10)).subplots_adjust(bottom=0.25)
  dendrogram(
    linkage_matrix,
    leaf_rotation=90.,
    leaf_font_size=16.,
    labels = labels,
  )
  plt.show()
  root, node_list = to_tree(linkage_matrix, rd=True)
  num_clusters = input("number of clusters: ")
  heap = []
  heapq.heappush(heap, (1/root.dist, root))
  while len(heap) < num_clusters:
    current = heapq.heappop(heap)[1]
    heapq.heappush(heap, (1/current.left.dist, current.left))
    heapq.heappush(heap, (1/current.right.dist, current.right))
  num_cats = 0
  for cluster in heap:
    dir_name = "cat" + str(num_cats) + "/"
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    else:
      rmtree(dir_name)
      os.mkdir(dir_name)
    num_cats += 1
    create_category(
      linkage_matrix,
      cluster[1],
      labels,
      src="generatedpictures",
      dest=dir_name
    )

main()
