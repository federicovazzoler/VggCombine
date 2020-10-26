import CombineHarvester.CombineTools.plotting as plot
import ROOT
from ROOT import TMath
import argparse
import sys

def createRatio(h1, h2):
  h3 = h1.Clone("h3")
  h3.SetLineColor(h1.GetMarkerColor())
  h3.SetMarkerStyle(20)
  h3.SetTitle("")
  #h3.SetMinimum(0.8)
  #h3.SetMaximum(1.2)
  # Set up plot for markers and errors
  #h3.Sumw2()
  h3.SetStats(0)
  h3.Divide(h2)
  
  # Adjust y-axis settings
  y = h3.GetYaxis()
  #y.SetTitle('ratio {0} / {1}'.format(h1.GetTitle(), h2.GetTitle()))
  y.SetTitle('prefit/postfit')
  y.SetNdivisions(505)
  y.SetTitleSize(20)
  y.SetTitleFont(43)
  y.SetTitleOffset(1.55)
  y.SetLabelFont(43)
  y.SetLabelSize(15)
  
  # Adjust x-axis settings
  x = h3.GetXaxis()
  x.SetTitleSize(20)
  x.SetTitleFont(43)
  x.SetTitleOffset(4.0)
  x.SetLabelFont(43)
  x.SetLabelSize(15)
  x.SetTitle('')
  
  return h3

def createCanvasPads(nPads):
  c = ROOT.TCanvas("c", "canvas", 800, 1000)
  padList = []  
  # Upper histogram plot is pad1
  padList.append(ROOT.TPad("pad1", "pad1", 0.0, 0.4, 1.0, 1.0))
  padList[0].SetBottomMargin(0.2)  # joins upper and lower plot
  padList[0].SetGridx()
  padList[0].SetGridy()
  padList[0].Draw()
  c.cd()

  for nPad in range(1, nPads+1):
    padList.append(ROOT.TPad('pad{0}'.format(nPad), 'pad{0}'.format(nPad), 0, 0.0 + 0.12*(nPad - 1), 1, 0.12 + 0.12*(nPad - 1)))
    padList[nPad].SetTopMargin(0.1)  # joins upper and lower plot
    padList[nPad].SetBottomMargin(0.2)
    padList[nPad].SetGridx()
    padList[nPad].SetGridy()
    padList[nPad].Draw()
 
  c.cd()
   
  return c, padList

# some initialisations
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-input_file', help='')
parser.add_argument('-channel', help='')
parser.add_argument('-output_folder', help='')
args = parser.parse_args()

# open file and take histo
fin = ROOT.TFile(args.input_file + '.root')

### PREFIT DISTRIBUTIONS ###
# data prefit
h_data_prefit = fin.Get('shapes_prefit' + '/' + args.channel + '/data')

# sig prefit
h_sig_prefit = fin.Get('shapes_prefit' + '/' + args.channel + '/diboson')
h_sig_prefit.SetLineColor(6)
h_sig_prefit.SetMarkerColor(6)
h_sig_prefit.SetMarkerStyle(20)
h_sig_prefit.SetMarkerSize(1)
h_sig_prefit.GetXaxis().SetTitle("Diphoton p_{T}")

# bkg prefit
my_list_prefit = fin.Get('shapes_prefit' + '/' + args.channel).GetListOfKeys()
h_bkg_prefit = []
for my_index in range(0, len(my_list_prefit)):
  if 'bkg' in my_list_prefit[my_index].GetName(): h_bkg_prefit.append(fin.Get('shapes_prefit' + '/' + args.channel + '/' + my_list_prefit[my_index].GetName()))

# lo style si vede
for my_index in range(0, len(h_bkg_prefit)):
  h_bkg_prefit[my_index].SetLineColor(2 + my_index)
  h_bkg_prefit[my_index].SetMarkerColor(2 + my_index)
  h_bkg_prefit[my_index].SetMarkerStyle(20)
  h_bkg_prefit[my_index].SetMarkerSize(1)
  h_bkg_prefit[my_index].GetXaxis().SetTitle("Diphoton p_{T}")

# hstack_prefit
hstack_mc_prefit = ROOT.THStack ("hstack_mc_prefit","hstack_mc_prefit")
for my_index in range(0, len(h_bkg_prefit)):
  hstack_mc_prefit.Add(h_bkg_prefit[my_index])
 
hstack_mc_prefit.Add(h_sig_prefit)
hstack_mc_prefit.SetMaximum(TMath.MaxElement(h_data_prefit.GetN(),h_data_prefit.GetY()) * 1.2)

### POSTFIT DISTRIBUTIONS ###
# data postfit
h_data_postfit = fin.Get('shapes_fit_s' + '/' + args.channel + '/data')

# sig postfit
h_sig_postfit = fin.Get('shapes_fit_s' + '/' + args.channel + '/diboson')
h_sig_postfit.SetLineColor(6)
h_sig_postfit.SetMarkerColor(6)
h_sig_postfit.SetMarkerStyle(24)
h_sig_postfit.SetMarkerSize(1)
h_sig_postfit.GetXaxis().SetTitle("Diphoton p_{T}")

# bkg postfit
my_list_postfit = fin.Get('shapes_fit_s' + '/' + args.channel).GetListOfKeys()
h_bkg_postfit = []
for my_index in range(0, len(my_list_postfit)):
  if 'bkg' in my_list_postfit[my_index].GetName(): h_bkg_postfit.append(fin.Get('shapes_fit_s' + '/' + args.channel + '/' + my_list_postfit[my_index].GetName()))

# lo style si vede
for my_index in range(0, len(h_bkg_postfit)):
  h_bkg_postfit[my_index].SetLineColor(2 + my_index)
  h_bkg_postfit[my_index].SetMarkerColor(2 + my_index)
  h_bkg_postfit[my_index].SetMarkerStyle(24)
  h_bkg_postfit[my_index].SetMarkerSize(1)
  h_bkg_postfit[my_index].GetXaxis().SetTitle("Diphoton p_{T}")

# hstack_postfit
hstack_mc_postfit = ROOT.THStack ("hstack_mc_postfit","hstack_mc_postfit")
for my_index in range(0, len(h_bkg_prefit)):
  hstack_mc_postfit.Add(h_bkg_postfit[my_index])
 
hstack_mc_postfit.Add(h_sig_postfit)
hstack_mc_postfit.SetMaximum(TMath.MaxElement(h_data_prefit.GetN(),h_data_prefit.GetY()) * 1.2)

# ratio plots
h_sig_ratio = createRatio(h_sig_prefit, h_sig_postfit)
h_sig_ratio.GetYaxis().SetRangeUser(h_sig_ratio.GetMinimum() - 0.1, h_sig_ratio.GetMaximum() + 0.1);

print h_sig_prefit.GetBinContent(1)
print h_sig_postfit.GetBinContent(1)
print h_sig_ratio.GetBinContent(1)
print ''
print h_sig_prefit.GetBinContent(2)
print h_sig_postfit.GetBinContent(2)
print h_sig_ratio.GetBinContent(2)

h_bkg_ratio = []
for my_index in range(0, len(h_bkg_prefit)):
  h_bkg_ratio.append(createRatio(h_bkg_prefit[my_index], h_bkg_postfit[my_index]))
  h_bkg_ratio[my_index].GetYaxis().SetRangeUser(h_bkg_ratio[my_index].GetMinimum() - 0.5, h_bkg_ratio[my_index].GetMaximum() + 0.5);

c, padList = createCanvasPads(len(h_bkg_ratio)+1)

# draw everything

c.cd()
padList[0].cd()

hstack_mc_postfit.Draw("PX")
#h_data_prefit.Draw('PSAME')
hstack_mc_prefit.Draw("SAME PX")
hstack_mc_prefit.GetXaxis().SetTitle("Diphoton p_{T}")
hstack_mc_prefit.GetYaxis().SetTitle("Events")
c.Update()

l_hstack_mc = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, '', 'NBNDC')
#l_hstack_mc.AddEntry(h_data_prefit, 'Data', 'P')
l_hstack_mc.AddEntry(h_sig_prefit, 'Signal', 'F')
for my_index in range(0, len(h_bkg_prefit)):
  l_hstack_mc.AddEntry(h_bkg_prefit[my_index], h_bkg_prefit[my_index].GetTitle(), 'F')
l_hstack_mc.Draw('SAME')
padList[0].Update()
c.Update()

c.cd()
for my_index in range(1, len(h_bkg_ratio)+1):
  padList[my_index].cd()
  h_bkg_ratio[my_index-1].Draw("EPX0")
  padList[my_index].Update()
  c.Update()
  c.cd()

padList[len(h_bkg_ratio)+1].cd()
h_sig_ratio.Draw("EPX0")
padList[len(h_bkg_ratio)+1].Update()
c.Update()
c.cd()

c.SaveAs(args.output_folder + '/' + args.input_file + '_COMPARISONS' + '.pdf')
