import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

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
h_diboson_systUp.SetMaximum(h_diboson_systUp.GetMaximum() * 1.2)

c_all.cd(2)
h_bkg_jetpho_misid_systUp.SetLineColor(ROOT.kRed)
h_bkg_jetpho_misid_systDown.SetLineColor(ROOT.kGreen)
h_bkg_jetpho_misid_systUp.Draw()
h_bkg_jetpho_misid.Draw('SAME')
h_bkg_jetpho_misid_err.Draw('E2SAME')
h_bkg_jetpho_misid_systDown.Draw('SAME')
h_bkg_jetpho_misid_systUp.SetMaximum(h_bkg_jetpho_misid_systUp.GetMaximum() * 1.2)

c_all.cd(3)
h_bkg_irred_systUp.SetLineColor(ROOT.kRed)
h_bkg_irred_systDown.SetLineColor(ROOT.kGreen)
h_bkg_irred_systUp.Draw()
h_bkg_irred.Draw('SAME')
h_bkg_irred_err.Draw('E2SAME')
h_bkg_irred_systDown.Draw('SAME')
h_bkg_irred_systUp.SetMaximum(h_bkg_irred_systUp.GetMaximum() * 1.2)

if boson == 'WGG':
  c_all.cd(4)
  h_bkg_egmisid_systUp.SetLineColor(ROOT.kRed)
  h_bkg_egmisid_systDown.SetLineColor(ROOT.kGreen)
  h_bkg_egmisid_systUp.Draw()
  h_bkg_egmisid.Draw('SAME')
  h_bkg_egmisid_err.Draw('E2SAME')
  h_bkg_egmisid_systDown.Draw('SAME')
  h_bkg_egmisid_systUp.SetMaximum(h_bkg_egmisid_systUp.GetMaximum() * 1.2)


c_all.SaveAs('html/combine_plots/syst_shape_plot/' + boson + '/' + channel + '/' + year + '/' + boson + '_' + channel + '_' + syst + '.pdf') 
