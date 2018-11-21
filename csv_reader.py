import csv
import pdb
import os

current_path = os.getcwd()
file_name = "ivan_mnist.csv"
file_path = current_path+"/test_result/"+file_name
with open(file_path, mode='r') as infile:
    reader = csv.reader(infile)
    with open(file_path, mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]:rows[1] for rows in reader}

pdb.set_trace()
