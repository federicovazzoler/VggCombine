import CombineHarvester.CombineTools.plotting as plot
import ROOT
from ROOT import TMath

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()

import sys
boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]
nToys = sys.argv[4]

f_data = ROOT.TFile.Open(boson + "_" + channel + "_" + year + "_GoodnessOfFit.root")
f_toys = ROOT.TFile.Open(boson + "_" + channel + "_" + year + "_GoodnessOfFit_toys.root")

t_data = f_data.Get("limit")
t_toys = f_toys.Get("limit")

for event in f_data.limit :
  lambda_0 = event.limit

num = 0
for event in f_toys.limit :
  if event.limit > lambda_0 :
    num = num + 1

p_value = float(num)/float(nToys)

output_file  = open(boson + "_" + channel + "_" + year + "_" + "p_value.txt","w")

output_file.write("Measured lambda_0 : %2f\n" % lambda_0)
output_file.write("Number of toys    : %i\n" % int(nToys))
output_file.write("Measured p_value  : %2f\n" % p_value)

output_file.close()
