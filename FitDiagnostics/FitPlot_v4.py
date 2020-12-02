import CombineHarvester.CombineTools.plotting as plot
import ROOT
from ROOT import TMath
import argparse
import sys

def maxValueYaxis(h_systUp, h_systDown):
  maxValueUp = 0
  maxValueDown = 0

  for i in range(1, h_systUp.GetNbinsX()):
    if h_systUp.GetBinContent(i) > maxValueUp: maxValueUp = h_systUp.GetBinContent(i)
    if h_systDown.GetBinContent(i) > maxValueDown: maxValueDown = h_systDown.GetBinContent(i)

  if maxValueUp > maxValueDown: return maxValueUp
  else: return maxValueDown

# some initialisations
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-boson', help='')
parser.add_argument('-channel', help='')
parser.add_argument('-year', help='')
parser.add_argument('-syst', help='')
parser.add_argument('-input_file_postfit', help='')
parser.add_argument('-output_folder', help='')
args = parser.parse_args()

# open files and take histos
f_prefit  = ROOT.TFile('../cards/' + args.boson + '_' + args.channel + '_' + args.year + '.root')
f_postfit = ROOT.TFile(args.input_file_postfit + '.root')

### PREFIT DISTRIBUTIONS ###
h_nominal = f_prefit.Get('bkg_jetpho_misid')
h_nominal.GetXaxis().SetTitle("p_{T}^{#gamma#gamma}")
h_nominal.SetLineStyle(1)
h_nominal.SetLineColor(1)
h_nominal.SetMarkerStyle(20)
h_nominal.SetMarkerColor(1)
h_nominal.SetMarkerSize(0)

h_syst_up = f_prefit.Get('bkg_jetpho_misid_' + args.syst + 'Up')
h_syst_up.GetXaxis().SetTitle("p_{T}^{#gamma#gamma}")
h_syst_up.SetLineStyle(1)
h_syst_up.SetLineColor(2)
h_syst_up.SetMarkerStyle(20)
h_syst_up.SetMarkerColor(2)
h_syst_up.SetMarkerSize(0)

h_syst_down = f_prefit.Get('bkg_jetpho_misid_' + args.syst + 'Down')
h_syst_down.GetXaxis().SetTitle("p_{T}^{#gamma#gamma}")
h_syst_down.SetLineStyle(1)
h_syst_down.SetLineColor(3)
h_syst_down.SetMarkerStyle(20)
h_syst_down.SetMarkerColor(3)
h_syst_down.SetMarkerSize(0)

### POSTFIT DISTRIBUTION ###
h_postfit = f_postfit.Get('shapes_fit_s' + '/' + args.channel + '/' + 'bkg_jetpho_misid')
h_postfit.GetXaxis().SetTitle("p_{T}^{#gamma#gamma}")
h_postfit.SetLineStyle(1)
h_postfit.SetLineColor(6)
h_postfit.SetMarkerStyle(24)
h_postfit.SetMarkerColor(6)
h_postfit.SetMarkerSize(0)

### CANVAS ###
c = ROOT.TCanvas()
c.cd()
h_nominal.Draw('HIST')
h_syst_up.Draw('HIST SAME')
h_syst_down.Draw('HIST SAME')
h_postfit.Draw('E0 SAME')
max_value = maxValueYaxis(h_syst_up, h_syst_down)
h_nominal.SetMaximum(max_value * 1.5)

leg = ROOT.TLegend(0.65, 0.640, 0.91, 0.88);
leg.SetBorderSize(0);
leg.SetEntrySeparation(0.01);
leg.SetFillColor(0);
leg.SetFillStyle(0);
leg.AddEntry(h_nominal, "prefit reference", "f");
leg.AddEntry(h_syst_up, "prefit syst up", "f");
leg.AddEntry(h_syst_down, "prefit syst down", "f");
leg.AddEntry(h_postfit, "postfit reference", "f");
leg.Draw()

c.Update()
c.SaveAs(args.output_folder + '/' + args.input_file_postfit + '_' + args.syst + '_PRE_vs_POST' + '.pdf')
