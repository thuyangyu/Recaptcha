import json
import pdb

data = {}

data['1'] = 2

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

with open('data.json') as data_file:
    data_loaded = json.load(data_file)

pdb.set_trace()
