import CombineHarvester.CombineTools.plotting as plot
import ROOT
from ROOT import TMath
import sys

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(width=700, l=0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)

boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]
nToys = sys.argv[4]

canvas = ROOT.TCanvas("canvas","canvas",10, 10, 800, 600)
canvas.cd()
pads = plot.OnePad()

f_toys = ROOT.TFile.Open(boson + "_" + channel + "_" + year + "_GoodnessOfFit_toys.root")
t_toys = f_toys.Get("limit")

vals = []
for e in range(t_toys.GetEntries()):
    t_toys.GetEntry(e)
    vals.append(t_toys.limit)

t_toys.Draw('limit>>hist(30,0,30)')
hist = ROOT.gDirectory.Get('hist')
hist.SetTitle('Test-statistic distribution')
hist.GetXaxis().SetTitle("#lambda")
hist.GetYaxis().SetTitle("events")
hist.Draw("HIST")

f_data = ROOT.TFile.Open(boson + "_" + channel + "_" + year + "_GoodnessOfFit.root")
t_data = f_data.Get("limit")

t_data.GetEntry(0)
obs = t_data.limit

pval = sum(1.0 for i in vals if i >= obs) / float(len(vals))

arr = ROOT.TArrow(obs, 0.001, obs, hist.GetMaximum()/4, 0.02, "<|")
arr.SetLineColor(ROOT.kBlue)
arr.SetFillColor(ROOT.kBlue)
arr.SetFillStyle(1001)
arr.SetLineWidth(6)
arr.SetLineStyle(1)
arr.SetAngle(60)
arr.Draw("<|same")

pt = ROOT.TPaveText(0.6,0.7,0.8,0.9,"NDCNB");
pt.AddText("num. toys : %i" % int(nToys));
pt.AddText("#lambda_{0} : %.2f" % float(obs));
pt.AddText("p-value : %.2f" % pval);
pt.Draw('same');

plot.DrawCMSLogo(pads[0], "CMS", "Preliminary", 11, 0.045, 0.035, 1.2,  cmsTextSize = 1.)

canvas.SaveAs(boson + "_" + channel + "_" + year + "_" + "p_value.pdf")

output_file  = open(boson + "_" + channel + "_" + year + "_" + "p_value.txt","w")

output_file.write("Number of toys  : %i\n" % int(nToys))
output_file.write("Lambda_0        : %f\n" % float(obs))
output_file.write("p-value for obs : %f\n" % float(pval))

output_file.close()
