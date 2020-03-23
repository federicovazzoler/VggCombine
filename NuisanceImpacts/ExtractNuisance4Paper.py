import json
import sys

boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]

with open(boson + '_' + channel + '_' + year + '_impacts.json') as f:
  data = json.load(f)

#sort to find longest string
data['params'].sort(key=lambda x: len(x['name']), reverse=True)
spaces = int(len(data['params'][1]['name']))

#sort to find largest syst
data['params'].sort(key=lambda x: abs(x['impact_r']), reverse=True)

output_file  = open(boson + "_" + channel + "_" + year + "_" + "syst_unc.txt","w")

for p in xrange(len(data['params'])):
  output_file.write("%s : %.2d %%\n" % (data['params'][p]['name'].ljust(spaces), float(data['params'][p]['impact_r']) * 100))

output_file.close()
