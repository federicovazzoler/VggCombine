import os
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
folder = sys.argv[1]
folder += '/'
boson = sys.argv[2]
channel = sys.argv[3]
year = sys.argv[4]
syst = sys.argv[5]

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

c_all.SaveAs(folder + boson + '/' + channel + '/' + year + '/' + boson + '_' + channel + '_' + syst + '.pdf') 


# pre-fit unc

sum_nevt = 0

nevt_diboson = h_diboson.Integral(0, h_diboson.GetNbinsX()+1)
sum_nevt += nevt_diboson
nevt_bkg_jetpho_misid = h_bkg_jetpho_misid.Integral(0, h_bkg_jetpho_misid.GetNbinsX()+1)
sum_nevt += nevt_bkg_jetpho_misid
nevt_bkg_irred = h_bkg_irred.Integral(0, h_bkg_irred.GetNbinsX()+1)
sum_nevt += nevt_bkg_irred
if boson == 'WGG': 
  nevt_bkg_egmisid = h_bkg_egmisid.Integral(0, h_bkg_egmisid.GetNbinsX()+1)
  sum_nevt += nevt_bkg_egmisid

sum_nevt_systUp = 0

nevt_diboson_systUp = h_diboson_systUp.Integral(0, h_diboson_systUp.GetNbinsX()+1)
sum_nevt_systUp += nevt_diboson_systUp 
nevt_bkg_jetpho_misid_systUp = h_bkg_jetpho_misid_systUp.Integral(0, h_bkg_jetpho_misid_systUp.GetNbinsX()+1)
sum_nevt_systUp += nevt_bkg_jetpho_misid_systUp 
nevt_bkg_irred_systUp = h_bkg_irred_systUp.Integral(0, h_bkg_irred.GetNbinsX()+1)
sum_nevt_systUp += nevt_bkg_irred_systUp 
if boson == 'WGG': 
  nevt_bkg_egmisid_systUp = h_bkg_egmisid_systUp.Integral(0, h_bkg_egmisid_systUp.GetNbinsX()+1)
  sum_nevt_systUp += nevt_bkg_egmisid_systUp 

sum_nevt_systDown = 0

nevt_diboson_systDown = h_diboson_systDown.Integral(0, h_diboson_systDown.GetNbinsX()+1)
sum_nevt_systDown += nevt_diboson_systDown 
nevt_bkg_jetpho_misid_systDown = h_bkg_jetpho_misid_systDown.Integral(0, h_bkg_jetpho_misid_systDown.GetNbinsX()+1)
sum_nevt_systDown += nevt_bkg_jetpho_misid_systDown 
nevt_bkg_irred_systDown = h_bkg_irred_systDown.Integral(0, h_bkg_irred.GetNbinsX()+1)
sum_nevt_systDown += nevt_bkg_irred_systDown 
if boson == 'WGG': 
  nevt_bkg_egmisid_systDown = h_bkg_egmisid_systDown.Integral(0, h_bkg_egmisid_systDown.GetNbinsX()+1)
  sum_nevt_systDown += nevt_bkg_egmisid_systDown 

output_file = open(folder + boson + '/' + channel + '/' + year + '/' + boson + '_' + channel + '_' + syst + '.txt','w')

output_file.write('Sum MC reference: {0}\n'.format(sum_nevt))
output_file.write('Sum MC SystUp   : {0}\n'.format(sum_nevt_systUp))
output_file.write('Sum MC SystDown : {0}\n'.format(sum_nevt_systDown))
output_file.write('Effect Up       : {0:.2f} %\n'.format((sum_nevt_systUp/sum_nevt - 1) * 100))
output_file.write('Effect Down     : {0:.2f} %\n'.format((sum_nevt_systDown/sum_nevt - 1) * 100))
if syst == 'jet_misid':
  output_file.write('Effect stat     : {0:.2f} %\n'.format(float((sum_nevt + h_bkg_jetpho_misid.GetBinError(0) + h_bkg_jetpho_misid.GetBinError(1) + h_bkg_jetpho_misid.GetBinError(2) + h_bkg_jetpho_misid.GetBinError(3) + h_bkg_jetpho_misid.GetBinError(4))/sum_nevt)))
  
#output_file.write('Effect avg      : {0:.2f} %%\n'.format(abs((sum_nevt_systUp/sum_nevt - 1) + (sum_nevt_systDown/sum_nevt - 1)) * 100))
