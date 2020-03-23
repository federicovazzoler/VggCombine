import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import sys
boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]

fin = ROOT.TFile('cards/' + boson + '_' + channel + '_' + year + '.root')

#grep number of events 4 ps
output_file  = open(boson + "_" + channel + "_" + year + "_" + "events_table.txt","w")

output_file.write(" PROCESS     | EVENTS  \n")
output_file.write(" --------------------- \n")
output_file.write(" observation | %.2f    \n" % float(fin.Get('data_obs').Integral()))
output_file.write(" signal      | %.2f    \n" % float(fin.Get('diboson').Integral()))
output_file.write(" bkg_jetpho  | %.2f    \n" % float(fin.Get('bkg_jetpho_misid').Integral()))
output_file.write(" bkg_irred   | %.2f    \n" % float(fin.Get('bkg_irred').Integral()))
if boson == 'WGG': output_file.write(" bkg_eg      | %.2f\n" % float(fin.Get('bkg_egmisid').Integral()))

output_file.close()
