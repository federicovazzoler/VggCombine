import ROOT

def maxValueYaxis(h_systUp, h_systDown):
  maxValueUp = 0
  maxValueDown = 0
  
  for i in range(1, h_systUp.GetNbinsX()):
    if h_systUp.GetBinContent(i) > maxValueUp: maxValueUp = h_systUp.GetBinContent(i)
    if h_systDown.GetBinContent(i) > maxValueDown: maxValueDown = h_systDown.GetBinContent(i)
  
  if maxValueUp > maxValueDown: return maxValueUp
  else: return maxValueDown

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

import sys
boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]
syst = sys.argv[4]

fin = ROOT.TFile('cards/' + boson + '_' + channel + '_' + year + '.root')

#nominal
h_diboson = fin.Get('diboson')
h_bkg_jetpho_misid = fin.Get('bkg_jetpho_misid')
h_bkg_irred = fin.Get('bkg_irred')
if boson == 'WGG': h_bkg_egmisid = fin.Get('bkg_egmisid')

#stat err on nominal
h_diboson_err = h_diboson.Clone()
h_bkg_jetpho_misid_err = h_bkg_jetpho_misid.Clone()
h_bkg_irred_err = h_bkg_irred.Clone()
if boson == 'WGG': h_bkg_egmisid_err = h_bkg_egmisid.Clone()

h_diboson_err.SetFillColorAlpha(12, 0.3)
h_bkg_jetpho_misid_err.SetFillColorAlpha(12, 0.3)
h_bkg_irred_err.SetFillColorAlpha(12, 0.3)
if boson == 'WGG': h_bkg_egmisid_err.SetFillColorAlpha(12, 0.3)

h_diboson_err.SetMarkerSize(0)
h_bkg_jetpho_misid_err.SetMarkerSize(0)
h_bkg_irred_err.SetMarkerSize(0)
if boson == 'WGG': h_bkg_egmisid_err.SetMarkerSize(0)

#systUp
h_diboson_systUp = fin.Get('diboson_' + syst + 'Up')
h_bkg_jetpho_misid_systUp = fin.Get('bkg_jetpho_misid_' + syst + 'Up')
h_bkg_irred_systUp = fin.Get('bkg_irred_' + syst + 'Up')
if boson == 'WGG': h_bkg_egmisid_systUp = fin.Get('bkg_egmisid_' + syst + 'Up')

#systDown
h_diboson_systDown = fin.Get('diboson_' + syst + 'Down')
h_bkg_jetpho_misid_systDown = fin.Get('bkg_jetpho_misid_' + syst + 'Down')
h_bkg_irred_systDown = fin.Get('bkg_irred_' + syst + 'Down')
if boson == 'WGG': h_bkg_egmisid_systDown = fin.Get('bkg_egmisid_' + syst + 'Down')

h_diboson_systUp.SetTitle('diboson')
h_bkg_jetpho_misid_systUp.SetTitle('bkg_jetpho_misid')
h_bkg_irred_systUp.SetTitle('irred')
if boson == 'WGG': h_bkg_egmisid_systUp.SetTitle('bkg_egmisid')

#canvases
c_all = ROOT.TCanvas()
c_all.Divide(2,2)

c_all.cd(1)
h_diboson_systUp.SetLineColor(ROOT.kRed)
h_diboson_systDown.SetLineColor(ROOT.kGreen)
h_diboson_systUp.Draw()
h_diboson.Draw('SAME')
h_diboson_err.Draw('E2SAME')
h_diboson_systDown.Draw('SAME')
MaxValue_h_diboson = maxValueYaxis(h_diboson_systUp, h_diboson_systDown)
h_diboson_systUp.SetMaximum(MaxValue_h_diboson * 1.2)

leg1 = ROOT.TLegend(0.65, 0.640, 0.91, 0.88);
leg1.SetBorderSize(0);
leg1.SetEntrySeparation(0.01);
leg1.SetFillColor(0);
leg1.SetFillStyle(0);
leg1.AddEntry(h_diboson_systDown, "Down", "f");
leg1.AddEntry(h_diboson_systUp, "Up", "f");

leg1.Draw()
c_all.Update()

c_all.cd(2)
h_bkg_jetpho_misid_systUp.SetLineColor(ROOT.kRed)
h_bkg_jetpho_misid_systDown.SetLineColor(ROOT.kGreen)
h_bkg_jetpho_misid_systUp.Draw()
h_bkg_jetpho_misid.Draw('SAME')
h_bkg_jetpho_misid_err.Draw('E2SAME')
h_bkg_jetpho_misid_systDown.Draw('SAME')
MaxValue_h_bkg_jetpho_misid = maxValueYaxis(h_bkg_jetpho_misid_systUp, h_bkg_jetpho_misid_systDown)
h_bkg_jetpho_misid_systUp.SetMaximum(MaxValue_h_bkg_jetpho_misid * 1.2)

leg2 = ROOT.TLegend(0.65, 0.640, 0.91, 0.88);
leg2.SetBorderSize(0);
leg2.SetEntrySeparation(0.01);
leg2.SetFillColor(0);
leg2.SetFillStyle(0);
leg2.AddEntry(h_bkg_jetpho_misid_systDown, "Down", "f");
leg2.AddEntry(h_bkg_jetpho_misid_systUp, "Up", "f");

leg2.Draw()
c_all.Update()

c_all.cd(3)
h_bkg_irred_systUp.SetLineColor(ROOT.kRed)
h_bkg_irred_systDown.SetLineColor(ROOT.kGreen)
h_bkg_irred_systUp.Draw()
h_bkg_irred.Draw('SAME')
h_bkg_irred_err.Draw('E2SAME')
h_bkg_irred_systDown.Draw('SAME')
MaxValue_h_bkg_irred = maxValueYaxis(h_bkg_irred_systUp, h_bkg_irred_systDown)
h_bkg_irred_systUp.SetMaximum(MaxValue_h_bkg_irred * 1.2)

leg3 = ROOT.TLegend(0.65, 0.640, 0.91, 0.88);
leg3.SetBorderSize(0);
leg3.SetEntrySeparation(0.01);
leg3.SetFillColor(0);
leg3.SetFillStyle(0);
leg3.AddEntry(h_bkg_irred_systDown, "Down", "f");
leg3.AddEntry(h_bkg_irred_systUp, "Up", "f");

leg3.Draw()
c_all.Update()

if boson == 'WGG':
  c_all.cd(4)
  h_bkg_egmisid_systUp.SetLineColor(ROOT.kRed)
  h_bkg_egmisid_systDown.SetLineColor(ROOT.kGreen)
  h_bkg_egmisid_systUp.Draw()
  h_bkg_egmisid.Draw('SAME')
  h_bkg_egmisid_err.Draw('E2SAME')
  h_bkg_egmisid_systDown.Draw('SAME')
  MaxValue_h_bkg_egmisid = maxValueYaxis(h_bkg_egmisid_systUp, h_bkg_egmisid_systDown)
  h_bkg_egmisid_systUp.SetMaximum(MaxValue_h_bkg_egmisid * 1.2)

  leg4 = ROOT.TLegend(0.65, 0.640, 0.91, 0.88);
  leg4.SetBorderSize(0);
  leg4.SetEntrySeparation(0.01);
  leg4.SetFillColor(0);
  leg4.SetFillStyle(0);
  leg4.AddEntry(h_bkg_egmisid_systDown, "Down", "f");
  leg4.AddEntry(h_bkg_egmisid_systUp, "Up", "f");
  
  leg4.Draw()
  c_all.Update()

c_all.SaveAs('html/combine_plots/syst_shape_plot/' + boson + '/' + channel + '/' + year + '/' + boson + '_' + channel + '_' + syst + '.pdf') 
