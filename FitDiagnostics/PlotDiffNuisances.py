import CombineHarvester.CombineTools.plotting as plot
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#plot.ModTDRStyle()

import sys
input_file = sys.argv[1]
output_folder = sys.argv[2]

fin = ROOT.TFile(input_file + '.root')

fin.Get('asdf').SaveAs(output_folder + '/' + input_file + '_asdf.pdf')
fin.Get('nuisances').SaveAs(output_folder + '/' + input_file + '_nuisances.pdf')
fin.Get('post_fit_errs').SaveAs(output_folder + '/' + input_file + '_post_fit_errs.pdf')
