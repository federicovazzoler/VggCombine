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
h_sig.SetFillColor(5)
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

pad1 = ROOT.TPad("pad1","pad1",0.0,0.3,1.0,1.0)
pad1.SetBottomMargin(0.001)
pad1.Draw()
pad1.cd()

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

pad1.Update()
c_hstack_mc.Update()
c_hstack_mc.cd()

pad2 = ROOT.TPad("pad2","pad2",0.0,0.0,1.0,0.3)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.Draw()
pad2.cd()

########RATIO PULL###########

h_sum = h_sig.Clone()
for my_index in range(0, len(h_bkg)):
  h_sum.Add(h_bkg[my_index])

#h_pull = h_sum.Clone()
#h_pull.Reset()
h_pull = ROOT.TGraph()
for i in range(0, h_data.GetN()):
  my_bin = ROOT.Double(0.)
  my_bin_dat_value = ROOT.Double(0.)

  h_data.GetPoint(i, my_bin, my_bin_dat_value)
  my_bin_dat_err = h_data.GetErrorY(i)
  my_bin_mc_err = h_sum.GetBinError(i+1)

  my_bin_dat_value = (my_bin_dat_value - h_sum.GetBinContent(i+1)) / TMath.Sqrt(my_bin_dat_err*my_bin_dat_err + my_bin_mc_err*my_bin_mc_err)
  h_pull.SetPoint(i, my_bin, my_bin_dat_value)
  #print "bin ",i," value ",my_bin," ",my_bin_dat_value

#############################

h_pull.SetTitle("")
#h_pull.SetStats(ROOT.kFALSE)
h_pull.GetXaxis().SetTitleFont(42);
h_pull.GetXaxis().SetTitleSize(0.11);
h_pull.GetXaxis().SetTitleOffset(1.1);
h_pull.GetXaxis().SetLabelFont(42);
h_pull.GetXaxis().SetLabelSize(0.10);
h_pull.GetXaxis().SetTitle("Diphoton p_{T}")
h_pull.GetYaxis().SetTitle("Pull");
h_pull.GetYaxis().SetTitleSize(0.11);
h_pull.GetYaxis().SetTitleOffset(0.36);
h_pull.GetYaxis().SetLabelSize(0.1);
h_pull.GetYaxis().SetLabelOffset(0.01);
h_pull.GetYaxis().SetNdivisions(505);
h_pull.GetYaxis().SetRangeUser(-3.5, 3.5);
h_pull.SetMarkerStyle(5);
h_pull.SetMarkerSize(1)
h_pull.Draw("AP");

line = ROOT.TLine(h_pull.GetXaxis().GetXmin(), 0.0, h_pull.GetXaxis().GetXmax(), 0.0);
line.SetLineColor(ROOT.kRed);
line.SetLineWidth(2);
line.Draw();

c_hstack_mc.SaveAs(output_folder + '/' + input_file + '_' + stage + '_SEPARATED' + '.pdf')
