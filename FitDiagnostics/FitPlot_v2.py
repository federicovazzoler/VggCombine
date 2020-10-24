import CombineHarvester.CombineTools.plotting as plot
import ROOT
from ROOT import TMath

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()

import sys
input_file = sys.argv[1]
channel = sys.argv[2]
stage = sys.argv[3]
output_folder = sys.argv[4]
if len(sys.argv) > 5: isBlind = '_' + sys.argv[5]
else: isBlind = ''

fin = ROOT.TFile(input_file + '.root')

if stage == 'prefit': first_dir = 'shapes_prefit'
elif stage == 'postfit': first_dir = 'shapes_fit_s'

if channel == 'ch_ele': second_dir = 'ch_ele'
elif channel == 'ch_muo': second_dir = 'ch_muo'

my_list = fin.Get(first_dir + '/' + second_dir).GetListOfKeys()
h_data = fin.Get(first_dir + '/' + second_dir + '/data')
h_sig = fin.Get(first_dir + '/' + second_dir + '/diboson')
h_bkg = []
for my_index in range(0, len(my_list)):
  if 'bkg' in my_list[my_index].GetName(): h_bkg.append(fin.Get(first_dir + '/' + second_dir + '/' + my_list[my_index].GetName()))

hstack_mc = ROOT.THStack ("hstack_mc","hstack_mc")
for my_index in range(0, len(h_bkg)):
  h_bkg[my_index].SetFillColor(2 + my_index)
  h_bkg[my_index].GetXaxis().SetTitle("Diphoton p_{T}")
  hstack_mc.Add(h_bkg[my_index])

hstack_mc.Add(h_sig)
hstack_mc.SetMaximum(TMath.MaxElement(h_data.GetN(),h_data.GetY()) * 1.2)

c_hstack_mc = ROOT.TCanvas("c_hstack_mc","c_hstack_mc",10, 10, 800, 600)
c_hstack_mc.cd()

hstack_mc.Draw("HIST")
hstack_mc.GetXaxis().SetTitle("Diphoton p_{T}")
hstack_mc.GetYaxis().SetTitle("Events")
h_data.Draw('PSAME')

l_hstack_mc = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, '', 'NBNDC')
l_hstack_mc.AddEntry(h_data, 'Data', 'P')
l_hstack_mc.AddEntry(h_sig, 'Signal', 'F')
for my_index in range(0, len(h_bkg)):
  l_hstack_mc.AddEntry(h_bkg[my_index], h_bkg[my_index].GetTitle(), 'F')
l_hstack_mc.Draw('SAME')
c_hstack_mc.Update()
c_hstack_mc.cd()

c_hstack_mc.SaveAs(output_folder + '/' + input_file + '_' + stage + '_SEPARATED' + '.pdf')
