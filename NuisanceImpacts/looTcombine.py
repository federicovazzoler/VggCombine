#!/usr/bin/env python

import sys
import re
import json
import ROOT
import os

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
expSig = sys.argv[4]

POI = 'r'

paramList = all_free_parameters(ws, 'w', 'ModelConfig', POI)

#First fit to r with r fixed to 1 to obtain expected errors on r
print 'Doing param : ' + POI
print 'Launching combine as :'
print 'combine -M MultiDimFit -n _initialFit_Test --algo singles --redefineSignalPOIs {0} --rMin {1} --rMax {2} --robustFit 1 -m 200 -d {3} -t -1 --expectSignal {4}'.format(POI, rMin, rMax, ws, expSig)
os.system('combine -M MultiDimFit -n _initialFit_Test --algo singles --redefineSignalPOIs {0} --rMin {1} --rMax {2} --robustFit 1 -m 200 -d {3} -t -1 --expectSignal {4}'.format(POI, rMin, rMax, ws, expSig))

#Now every nuisance
for param in paramList:
  print ''
  print '-----------------------'
  print 'Doing param : ' + param
  print 'Launching combine as :'
  print 'combine -M MultiDimFit -n _paramFit_Test_{0} --algo impact --redefineSignalPOIs {1} -P {2} --floatOtherPOIs 1 --saveInactivePOI 1 --rMin {3} --rMax {4} --robustFit 1 -m 200 -d {5} -t -1 --expectSignal {6}'.format(param, POI, param, rMin, rMax, ws, expSig)
  os.system('combine -M MultiDimFit -n _paramFit_Test_{0} --algo impact --redefineSignalPOIs {1} -P {2} --floatOtherPOIs 1 --saveInactivePOI 1 --rMin {3} --rMax {4} --robustFit 1 -m 200 -d {5} -t -1 --expectSignal {6}'.format(param, POI, param, rMin, rMax, ws, expSig))
