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

canvas = ROOT.TCanvas("canvas","canvas",10, 10, 800, 600)
canvas.cd()

fin = ROOT.TFile(input_file + '.root')

if stage == 'prefit': first_dir = 'shapes_prefit'
elif stage == 'postfit': first_dir = 'shapes_fit_s'

if channel == 'ch_ele': second_dir = 'ch_ele'
elif channel == 'ch_muo': second_dir = 'ch_muo'

#get histograns
h_bkg = fin.Get(first_dir + '/' + second_dir + '/total_background')
h_sig = fin.Get(first_dir + '/' + second_dir + '/total_signal')
h_dat = fin.Get(first_dir + '/' + second_dir + '/data')  # This is a TGraphAsymmErrors, not a TH1F

pad1 = ROOT.TPad("pad1","pad1",0.0,0.3,1.0,1.0)
pad1.SetBottomMargin(0.001)
pad1.Draw()
pad1.cd()

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

pad1.Update()
canvas.Update()
canvas.cd()

pad2 = ROOT.TPad("pad2","pad2",0.0,0.0,1.0,0.3)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.Draw()
pad2.cd()

h_sum = h_bkg.Clone()
h_sum.Add(h_sig)
h_ratio = h_sum.Clone()
h_ratio.Reset()
nPoints = h_dat.GetN();
for i in range(0,nPoints):
  x = ROOT.Double(0.)
  y = ROOT.Double(0.)
  h_dat.GetPoint(i, x, y)
  h_ratio.Fill(x,y)

for i in range(0,h_ratio.GetNbinsX() + 1):
  h_ratio.SetBinError(i, TMath.Sqrt(h_ratio.GetBinContent(i)))   

h_ratio.Divide(h_sum)

h_ratio.SetTitle("")
h_ratio.SetStats(ROOT.kFALSE)

h_ratio.GetXaxis().SetTitleFont(42);
h_ratio.GetXaxis().SetTitleSize(0.11);
h_ratio.GetXaxis().SetTitleOffset(1.1);
h_ratio.GetXaxis().SetLabelFont(42);
h_ratio.GetXaxis().SetLabelSize(0.10);

h_ratio.GetYaxis().SetTitle("Data/MC");
h_ratio.GetYaxis().SetTitleSize(0.11);
h_ratio.GetYaxis().SetTitleOffset(0.36);
h_ratio.GetYaxis().SetLabelSize(0.1);
h_ratio.GetYaxis().SetLabelOffset(0.01);
h_ratio.GetYaxis().SetNdivisions(505);
h_ratio.GetYaxis().SetRangeUser(0.5, 1.5);

h_ratio.SetMarkerStyle(20);
h_ratio.Draw("E0PX0");

line = ROOT.TLine(h_ratio.GetXaxis().GetXmin(), 1.0, h_ratio.GetXaxis().GetXmax(), 1.0);
line.SetLineColor(ROOT.kRed);
line.SetLineWidth(2);
line.Draw();

canvas.SaveAs(output_folder + '/' + input_file + '_' + stage + isBlind + '.pdf')

#stack
hstack_mc = ROOT.THStack ("hstack_mc","hstack_mc")
hstack_mc.Add(h_bkg)
hstack_mc.Add(h_sig)
hstack_mc.SetMaximum(TMath.MaxElement(h_dat.GetN(),h_dat.GetY()) * 1.2)

c_hstack_mc = ROOT.TCanvas("c_hstack_mc","c_hstack_mc",10, 10, 800, 600)
c_hstack_mc.cd()

p1_hstack_mc = ROOT.TPad("p1_hstack_mc","p1_hstack_mc",0.0,0.3,1.0,1.0)
p1_hstack_mc.SetBottomMargin(0.001)
p1_hstack_mc.Draw()
p1_hstack_mc.cd()

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

p1_hstack_mc.Update()
c_hstack_mc.Update()
c_hstack_mc.cd()

p2_hstack_mc = ROOT.TPad("p2_hstack_mc","p2_hstack_mc",0.0,0.0,1.0,0.3)
p2_hstack_mc.SetTopMargin(0)
p2_hstack_mc.SetBottomMargin(0.3)
p2_hstack_mc.Draw()
p2_hstack_mc.cd()

h_ratio.Draw("E0PX0");
line.Draw();

c_hstack_mc.SaveAs(output_folder + '/' + input_file + '_' + stage + '_stack' + isBlind + '.pdf')
