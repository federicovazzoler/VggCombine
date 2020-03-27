#!/usr/bin/env python

import sys
import re
import json
import ROOT
import os
import glob

from CombineHarvester.CombineTools.combine.CombineToolBase import CombineToolBase
try:
    from HiggsAnalysis.CombinedLimit.RooAddPdfFixer import FixAll
except ImportError:
    #compatibility for combine version earlier than https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/tree/2d172ef50fccdfbbc2a499ac8e47bba2d667b95a
    #can delete in a few months
    def FixAll(workspace): pass

def all_free_parameters(file, wsp, mc, pois):
        res = []
        wsFile = ROOT.TFile.Open(file)
        w = wsFile.Get(wsp)
        FixAll(w)
        config = w.genobj(mc)
        pdfvars = config.GetPdf().getParameters(config.GetObservables())
        it = pdfvars.createIterator()
        var = it.Next()
        while var:
            if var.GetName() not in pois and (not var.isConstant()) and var.InheritsFrom("RooRealVar"):
                res.append(var.GetName())
            var = it.Next()
        return res

ws = sys.argv[1]
rMin = sys.argv[2]
rMax = sys.argv[3]
nPoints = sys.argv[4]
isBlind = sys.argv[5]
POI = 'r'

# is blind or not?
if isBlind == 'blind': 
  blindString = ' -t -1 --expectSignal 1'
elif isBlind == 'unblind':
  blindString = ''

# list of nuisances (for freezing) excluding stat errors from MC
paramList = all_free_parameters(ws, 'w', 'ModelConfig', POI)
paramList = [x for x in paramList if not x.startswith('prop_binch')]
paramList = ','.join(paramList)

# fit r
print '---------------------'
print 'Fit r'
print 'Launching combine as :'
print 'combine -M MultiDimFit {0} -m 200 --rMin {1} --rMax {2} --algo grid --points {3} --robustFit=1'.format(ws, rMin, rMax, nPoints) + blindString
os.system('combine -M MultiDimFit {0} -m 200 --rMin {1} --rMax {2} --algo grid --points {3} --robustFit=1'.format(ws, rMin, rMax, nPoints) + blindString)

# create snapshot
print ''
print '---------------------'
print 'Create snapshot'
print 'Launching combine as :'
print 'combine -M MultiDimFit {0} -n .snapshot -m 200 --rMin {1} --rMax {2} --saveWorkspace --robustFit=1'.format(ws, rMin, rMax) + blindString
os.system('combine -M MultiDimFit {0} -n .snapshot -m 200 --rMin {1} --rMax {2} --saveWorkspace --robustFit=1'.format(ws, rMin, rMax) + blindString)

# freeze stat and syst
print ''
print '---------------------'
print 'Freeze stat and syst'
mylist = ','.join(paramList)
print 'Launching combine as :'
print 'combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH200.root -n .freezeAll -m 200 --rMin {0} --rMax {1} --algo grid --points {2} --freezeParameters {3} --snapshotName MultiDimFit --robustFit=1'.format(rMin, rMax, nPoints, paramList) + blindString
os.system('combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH200.root -n .freezeAll -m 200 --rMin {0} --rMax {1} --algo grid --points {2} --freezeParameters {3} --snapshotName MultiDimFit --robustFit=1'.format(rMin, rMax, nPoints, paramList) + blindString)
