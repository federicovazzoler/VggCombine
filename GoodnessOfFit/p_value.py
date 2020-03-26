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

hist = ROOT.TH1D("hist","Lambda distribution",100,0.,20.)

for event in f_toys.limit :
  hist.Fill(event.limit)
  if event.limit > lambda_0 :
    num = num + 1

p_value = float(num)/float(nToys)

canvas = ROOT.TCanvas("canvas","canvas",10, 10, 800, 600)
canvas.cd()

#f_toys.limit.Draw("limit")
hist.GetXaxis().SetTitle("#lambda")
hist.GetYaxis().SetTitle("events")
hist.Draw()

pt = ROOT.TPaveText(0.6,0.7,0.8,0.9,"NDCNB");
pt.AddText("nToys  : %i" % int(nToys));
pt.AddText("pValue : %.2f" % p_value);
pt.Draw('same');

line = ROOT.TLine(lambda_0, 0., lambda_0, hist.GetMaximum()*0.5);
line.SetLineColor(ROOT.kRed);
line.SetLineWidth(2);
line.Draw("same");

canvas.SaveAs(boson + "_" + channel + "_" + year + "_" + "p_value.pdf")

p_value = p_value*100

output_file  = open(boson + "_" + channel + "_" + year + "_" + "p_value.txt","w")

output_file.write("Measured lambda_0 : %.2f\n" % lambda_0)
output_file.write("Number of toys    : %i\n" % int(nToys))
output_file.write("Measured p_value  : %.2f %%\n" % p_value)

output_file.close()
