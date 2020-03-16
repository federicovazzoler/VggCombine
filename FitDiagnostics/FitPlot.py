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

canvas = ROOT.TCanvas()

fin = ROOT.TFile(input_file + '.root')

if stage == 'prefit': first_dir = 'shapes_prefit'
elif stage == 'postfit': first_dir = 'shapes_fit_s'

if channel == 'ch_ele': second_dir = 'ch_ele'
elif channel == 'ch_muo': second_dir = 'ch_muo'

#get histograns
h_bkg = fin.Get(first_dir + '/' + second_dir + '/total_background')
h_sig = fin.Get(first_dir + '/' + second_dir + '/total_signal')
h_dat = fin.Get(first_dir + '/' + second_dir + '/data')  # This is a TGraphAsymmErrors, not a TH1F

h_bkg.SetFillColor(ROOT.TColor.GetColor(100, 192, 232))
h_bkg.GetXaxis().SetTitle("Diphoton p_{T}")
h_bkg.Draw('HIST')

h_err = h_bkg.Clone()
h_err.SetFillColorAlpha(12, 0.3)  # Set grey colour (12) and alpha (0.3)
h_err.SetMarkerSize(0)
h_err.Draw('E2SAME')

h_sig.SetLineColor(ROOT.kRed)
h_sig.Draw('HISTSAME')

h_err_sig = h_sig.Clone()
h_err_sig.SetFillColorAlpha(2, 0.3)  # Set grey colour (12) and alpha (0.3)
h_err_sig.SetMarkerSize(0)
h_err_sig.Draw('E2SAME')

h_dat.Draw('PSAME')

h_bkg.SetMaximum(TMath.MaxElement(h_dat.GetN(),h_dat.GetY()) * 1.2)

#signal strenght
tree = fin.Get('tree_fit_sb')
signal_strenght = tree.GetLeaf('r')
signal_strenght_HiErr = tree.GetLeaf('rHiErr')
signal_strenght_LoErr = tree.GetLeaf('rLoErr')
tree.GetEntry(0)
signal_strenght = signal_strenght.GetValue()
signal_strenght_HiErr = signal_strenght_HiErr.GetValue()
signal_strenght_LoErr = signal_strenght_LoErr.GetValue()

#pavetext
pt = ROOT.TPaveText(0.6,0.7,0.8,0.5,"NBNDC");
pt.AddText('#mu = ' + str(signal_strenght));
pt.AddText('#sigma_{#mu}^{up} = ' + str(signal_strenght_HiErr));
pt.AddText('#sigma_{#mu}^{down} = ' + str(signal_strenght_LoErr));
if stage == 'postfit': pt.Draw('SAME');

#legend
legend = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, '', 'NBNDC')
legend.AddEntry(h_dat, 'Data', 'P')
legend.AddEntry(h_sig, 'Signal', 'L')
legend.AddEntry(h_err_sig, 'Signal uncertainty', 'F')
legend.AddEntry(h_bkg, 'Background', 'F')
legend.AddEntry(h_err, 'Background uncertainty', 'F')
legend.Draw()

canvas.SaveAs(output_folder + '/' + input_file + '_' + stage + isBlind + '.pdf')

#stack
hstack_mc = ROOT.THStack ("hstack_mc","hstack_mc")
hstack_mc.Add(h_bkg)
hstack_mc.Add(h_sig)
hstack_mc.SetMaximum(TMath.MaxElement(h_dat.GetN(),h_dat.GetY()) * 1.2)

c_hstack_mc = ROOT.TCanvas()
hstack_mc.Draw("HIST")
hstack_mc.GetXaxis().SetTitle("Diphoton p_{T}")
hstack_mc.GetYaxis().SetTitle("Events")
h_dat.Draw('PSAME')

l_hstack_mc = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, '', 'NBNDC')
l_hstack_mc.AddEntry(h_dat, 'Data', 'P')
l_hstack_mc.AddEntry(h_sig, 'Signal', 'L')
l_hstack_mc.AddEntry(h_bkg, 'Background', 'F')
l_hstack_mc.Draw('SAME')
if stage == 'postfit': pt.Draw('SAME');

c_hstack_mc.SaveAs(output_folder + '/' + input_file + '_' + stage + '_stack' + isBlind + '.pdf')
