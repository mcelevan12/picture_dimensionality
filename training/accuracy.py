import os
import csv

def block_accoracy(modeling_file_name):
  modeling_file = open(modeling_file_name, "r")
  csv_reader = csv.reader(modeling_file, delimiter='\t')
  for row in csv_reader:



def main():
  data_dir = "./modeling/"
  for condition in os.listdir(data_dir):
    for modeling_file_name in os.listdir(os.path.join(data_dir, condition)):
      if modeling_file_name.endswith(".csv"):
        block_accuracy(os.path.join(data_dir, condition, modeling_file_name))

main()
