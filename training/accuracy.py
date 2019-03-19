import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import data

# there are 5 lights! (4 params + row)
def model_shift(dims):
  model_row = 1
  params = 4
  alphas = dims
  ws = 2*18
  return model_row + params + alphas + ws

def training(dims, training_file_name):
  training_file = open(training_file_name, "r")
  training_csv = csv.reader(training_file, delimiter=',')
  next(training_csv)
  training_examples = []
  for training_example in training_csv:
    training_examples.append(int(training_example[3 + dims]))
  return training_examples

def block_accuracy(training, model):
  block_sum = 0.0
  trials = 0
  block_acc = []
  for training_example, model_output in zip(training, model):
    trials += 1
    if model_output == 'NA':
      model_output = 1 # (hopefully) might wanna clean this up earlier
    if training_example:
      block_sum += float(model_output)
    else:
      block_sum += 1 - float(model_output)
    if trials % 18 == 0:
      block_acc.append(block_sum/18.0)
      block_sum = 0
  return block_acc

def sqr_error(blocks, responses):
  error = 0.0
  for model_block, response_block in zip(blocks, responses):
    error += (model_block - response_block) ** 2
  return error / (12)

def best_model_across_cats(dims, training_list, responses_list, modeling_list):
  smallest_error = 1000000
  best_model = -1
  #94710 is the number of models in each csv file
  for row_num in range(94710):
    error = 0
    for training, response, model_idx in zip(training_list, responses_list, range(len(modeling_list))):
      error += sqr_error(block_accuracy(training, next(modeling_list[model_idx])[model_shift(dims):]), responses_list[response]) # hope this works
    error = error/3.0
    if error < smallest_error:
      smallest_error = error
      best_model = row_num
    if row_num % 25000 == 0:
      print("iteration: " + str(row_num))
  return (smallest_error, best_model)

def main():
  modeling_dir = "./modeling"
  training_dir = "./training_data"
  models = defaultdict(list)
  trs = defaultdict(list)
  responses = data.avg_block_data()
  print(responses)
  if True:
    return False
  for condition in os.listdir(modeling_dir):
      for csv_file in os.listdir(os.path.join(modeling_dir, condition)):
        model_csv = csv.reader(open(os.path.join(modeling_dir, condition, csv_file), "r"), delimiter=',')
        next(model_csv) #remove header
        models[int(csv_file[3:5])].append(model_csv)
  for condition in os.listdir(training_dir):
      for csv_file in os.listdir(os.path.join(training_dir, condition)):
        trs[int(csv_file[3:5])].append(training(int(csv_file[3:5]), os.path.join(training_dir, condition, csv_file)))
  best = {}
  for dims in trs:
    print(trs[dims])
    print(models[dims])
    break
#    best[dims] = best_model_across_cats(dims, trs[dims], responses, models[dims])
#    print(dims)
#    print(best[dims])
#  print(best)
#    accuracies = calculate_block_accuracy(dims, data.avg_block_data(), trs[dims], models[dims])
#    plt.hist(accuracies, color = 'blue', edgecolor = 'black',
#         bins = int(180))
#    plt.show()

main()
