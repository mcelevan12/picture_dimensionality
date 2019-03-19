from __future__ import print_function
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import os

def image(path,zoom=0.25):
  return OffsetImage(plt.imread(path),zoom=zoom)

def pic_from_path(pic_path):
  return pic_path.split('/')[-1][:-4]

def _cats():
  cats = defaultdict(set)
  for root, dir, files in os.walk("/home/evan/Documents/picture_dimensionality/experiment_cats"):
    for filename in files:
      cats[root.split('/')[-1]].add(os.path.join(root, filename))
  return cats

def main():
  dir = "/home/evan/Documents/picture_dimensionality"
  cats = _cats()
  marks = ["s", "o", "v"]
  with open(os.path.join(dir, "training/reduced_data/PCA02.json"), 'r') as file:
    reduced_data = json.load(file)
    x = []
    y = []
    pics = []
    for pic_path in cats["all"]:
      x.append(reduced_data[pic_from_path(pic_path)][0])
      y.append(reduced_data[pic_from_path(pic_path)][1])
      pics.append(pic_path)
    fig, ax = plt.subplots(figsize=(19.2, 14.4))
    ax.scatter(x, y)
    for x0, y0, path in zip(x, y, pics):
      ab = AnnotationBbox(image(path, 0.2), (x0, y0), frameon=False)
      pics.append(ax.add_artist(ab))
    x = []
    y = []
    pics = []
    for cat in cats:
      if "all" not in cat and "rand" not in cat:
        for pic_path in cats[cat]:
          x.append(reduced_data[pic_from_path(pic_path)][0])
          y.append(reduced_data[pic_from_path(pic_path)][1])
          pics.append(pic_path)
    #          far: 0,      1
    #          near: 0,               2
    #          goldish      teal      purple
    colors = ['#ffa500', '#00ffa5', '#a500ff']
    for x0, y0, path in zip(x, y, pics):
      ab = AnnotationBbox(image(path, 0.3), (x0, y0), frameon=True, pad=0.0, bboxprops=dict(facecolor='none', edgecolor=colors[int(path.split('/')[-2][-1])], linewidth=8))
      pics.append(ax.add_artist(ab))
#    plt.show()
    plt.savefig("./picture_points_PCA02.png")

main()
