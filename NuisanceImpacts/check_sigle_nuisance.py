#!/usr/bin/env python
import ROOT
import sys
import re
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-ws', help='input workspace')
parser.add_argument('-rMin', help="minimum value of r (mu) for the fit")
parser.add_argument('-rMax', help="maximum value of r (mu) for the fit")
parser.add_argument('-o', help='output directory')
parser.add_argument('-expSig', help='expected value of mu 1 if blind. If None will run unblinded')
args = parser.parse_args()

if args.expSig == '0':
  print 'mu = 0 not supported'
  sys.exit()

toDo = 'combineTool.py -d {0} -M MultiDimFit --algo=grid --X-rtd OPTIMIZE_BOUND=0 --rMin {1} --rMax {2} --saveSpecifiedNuis all -n "name" --points 400 --trackParameters "rgx{{.*_norm_.*}}"'.format(args.ws, args.rMin, args.rMax) 

if args.expSig == None:
  print ''
  print '-----------------------'
  print 'UNBLIND FIT'
  print 'Launching combine as :'
  print toDo
  print '-----------------------'
  print ''
  os.system(toDo)
else:
  toDo += ' -t -1 --expectSignal {0}'.format(args.expSig)
  print ''
  print '-----------------------'
  print 'BLIND FIT - mu = {0}'.format(args.expSig)
  print 'Launching combine as :'
  print toDo
  print '-----------------------'
  print ''
  os.system(toDo)
