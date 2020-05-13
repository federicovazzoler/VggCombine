import sys
import os
import math
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

folder = sys.argv[1]
folder += '/'
year = sys.argv[2]

input_file = ['', '', '', '']

input_file[0] = ROOT.TFile('cards/WGG_ch_ele_' + year + '.root')
input_file[1] = ROOT.TFile('cards/WGG_ch_muo_' + year + '.root')
input_file[2] = ROOT.TFile('cards/ZGG_ch_ele_' + year + '.root')
input_file[3] = ROOT.TFile('cards/ZGG_ch_muo_' + year + '.root')

output_file  = open(folder + 'events_table_' + year + '.txt','w')

# 0-1 wgg ele (evt-stat err), 2-3 wgg muon, 4-5 zgg ele, 6-7 zgg muo
nevt_data_obs         = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_diboson          = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_bkg_jetpho_misid = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_bkg_irred        = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_bkg_egmisid      = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_sum_mc_bkg       = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]
nevt_sum_mc_tot       = [[ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)], [ROOT.Double(0), ROOT.Double(0)]]

data_obs_string = ['', '', '', '']
diboson_string = ['', '', '', '']
bkg_jetpho_misid_string = ['', '', '', '']
bkg_irred_string = ['', '', '', '']
bkg_egmisid_string = ['', '', '', '']
sum_mc_bkg_string = ['', '' ,'' ,'']
sum_mc_tot_string = ['', '' ,'' ,'']

for i in range(len(input_file)):
  nevt_data_obs[i][0] = input_file[i].Get('data_obs').IntegralAndError(0, input_file[i].Get('data_obs').GetNbinsX()+1, nevt_data_obs[i][1])

  if nevt_data_obs[i][0] != ROOT.Double(0):
    data_obs_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_data_obs[i][0], nevt_data_obs[i][1])
  else:
    data_obs_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(data_obs_string[i])):
    data_obs_string[i] += ' '

  nevt_diboson[i][0] = input_file[i].Get('diboson').IntegralAndError(0, input_file[i].Get('diboson').GetNbinsX()+1, nevt_diboson[i][1])
  nevt_sum_mc_tot[i][0] += nevt_diboson[i][0]
  nevt_sum_mc_tot[i][1] += pow(nevt_diboson[i][1], 2)

  if nevt_diboson[i][0] != ROOT.Double(0):
    diboson_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_diboson[i][0], nevt_diboson[i][1])
  else:
    diboson_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(diboson_string[i])):
    diboson_string[i] += ' '

  nevt_bkg_jetpho_misid[i][0] = input_file[i].Get('bkg_jetpho_misid').IntegralAndError(0, input_file[i].Get('bkg_jetpho_misid').GetNbinsX()+1, nevt_bkg_jetpho_misid[i][1])
  nevt_sum_mc_tot[i][0] += nevt_bkg_jetpho_misid[i][0]
  nevt_sum_mc_tot[i][1] += pow(nevt_bkg_jetpho_misid[i][1], 2)
  nevt_sum_mc_bkg[i][0] += nevt_bkg_jetpho_misid[i][0]
  nevt_sum_mc_bkg[i][1] += pow(nevt_bkg_jetpho_misid[i][1], 2)

  if nevt_bkg_jetpho_misid[i][0] != ROOT.Double(0):
    bkg_jetpho_misid_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_bkg_jetpho_misid[i][0], nevt_bkg_jetpho_misid[i][1])
  else:
    bkg_jetpho_misid_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(bkg_jetpho_misid_string[i])):
    bkg_jetpho_misid_string[i] += ' '

  nevt_bkg_irred[i][0] = input_file[i].Get('bkg_irred').IntegralAndError(0, input_file[i].Get('bkg_irred').GetNbinsX()+1, nevt_bkg_irred[i][1])
  nevt_sum_mc_tot[i][0] += nevt_bkg_irred[i][0]
  nevt_sum_mc_tot[i][1] += pow(nevt_bkg_irred[i][1], 2)
  nevt_sum_mc_bkg[i][0] += nevt_bkg_irred[i][0]
  nevt_sum_mc_bkg[i][1] += pow(nevt_bkg_irred[i][1], 2)

  if nevt_bkg_irred[i][0] != ROOT.Double(0):
    bkg_irred_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_bkg_irred[i][0], nevt_bkg_irred[i][1])
  else:
    bkg_irred_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(bkg_irred_string[i])):
    bkg_irred_string[i] += ' '
  
  if i < 2:
    nevt_bkg_egmisid[i][0] = input_file[i].Get('bkg_egmisid').IntegralAndError(0, input_file[i].Get('bkg_egmisid').GetNbinsX()+1, nevt_bkg_egmisid[i][1])
    nevt_sum_mc_tot[i][0] += nevt_bkg_egmisid[i][0]
    nevt_sum_mc_tot[i][1] += pow(nevt_bkg_egmisid[i][1], 2)
    nevt_sum_mc_bkg[i][0] += nevt_bkg_egmisid[i][0]
    nevt_sum_mc_bkg[i][1] += pow(nevt_bkg_egmisid[i][1], 2)

    if nevt_bkg_egmisid[i][0] != ROOT.Double(0):
      bkg_egmisid_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_bkg_egmisid[i][0], nevt_bkg_egmisid[i][1])
    else:
      bkg_egmisid_string[i] = ' n.a. +- n.a.'
    for sp in range(16 - len(bkg_egmisid_string[i])):
      bkg_egmisid_string[i] += ' '
  else :
    bkg_egmisid_string[i] = ' n.a. +- n.a.'
    for sp in range(16 - len(bkg_egmisid_string[i])):
      bkg_egmisid_string[i] += ' '
  
  nevt_sum_mc_tot[i][1] = math.sqrt(nevt_sum_mc_tot[i][1])
  nevt_sum_mc_bkg[i][1] = math.sqrt(nevt_sum_mc_bkg[i][1])

  if nevt_sum_mc_tot[i][0] != ROOT.Double(0):
    sum_mc_tot_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_sum_mc_tot[i][0], nevt_sum_mc_tot[i][1])
  else:
    sum_mc_tot_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(sum_mc_tot_string[i])):
    sum_mc_tot_string[i] += ' '
 
  if nevt_sum_mc_bkg[i][0] != ROOT.Double(0):
    sum_mc_bkg_string[i] = ' {0:.1f} +- {1:.1f}'.format(nevt_sum_mc_bkg[i][0], nevt_sum_mc_bkg[i][1])
  else:
    sum_mc_bkg_string[i] = ' n.a. +- n.a.'
  for sp in range(16 - len(sum_mc_bkg_string[i])):
    sum_mc_bkg_string[i] += ' '
  
# output in table style

output_file.write('|----------------|----------------|----------------|----------------|----------------|\n')
output_file.write('| PROCESS        | WGG ele        | WGG muo        | ZGG ele        | ZGG muo        |\n')
output_file.write('|----------------|----------------|----------------|----------------|----------------|\n')
output_file.write('| signal         |' + diboson_string[0] + '|' + diboson_string[1] + '|' + diboson_string[2] + '|' + diboson_string[3] + '|\n')
output_file.write('| jet misid      |' + bkg_jetpho_misid_string[0] + '|' + bkg_jetpho_misid_string[1] + '|' + bkg_jetpho_misid_string[2] + '|' + bkg_jetpho_misid_string[3] + '|\n')
output_file.write('| irred          |' + bkg_irred_string[0] + '|' + bkg_irred_string[1] + '|' + bkg_irred_string[2] + '|' + bkg_irred_string[3] + '|\n')
output_file.write('| eg misid       |' + bkg_egmisid_string[0] + '|' + bkg_egmisid_string[1] + '|' + bkg_egmisid_string[2] + '|' + bkg_egmisid_string[3] + '|\n')
output_file.write('|----------------|----------------|----------------|----------------|----------------|\n')
output_file.write('| sum mc bkg     |' + sum_mc_bkg_string[0] + '|' + sum_mc_bkg_string[1] + '|' + sum_mc_bkg_string[2] + '|' + sum_mc_bkg_string[3] + '|\n')
output_file.write('| sum mc tot     |' + sum_mc_tot_string[0] + '|' + sum_mc_tot_string[1] + '|' + sum_mc_tot_string[2] + '|' + sum_mc_tot_string[3] + '|\n')
output_file.write('|----------------|----------------|----------------|----------------|----------------|\n')
output_file.write('| data obs       |' + data_obs_string[0] + '|' + data_obs_string[1] + '|' + data_obs_string[2] + '|' + data_obs_string[3] + '|\n')
output_file.write('|----------------|----------------|----------------|----------------|----------------|\n')

output_file.close()

output_file_tex = open(folder + 'events_table_' + year + '_LATEX.txt','w')

output_file_tex.write('\\begin{table}\n')
output_file_tex.write('\centering\n')
output_file_tex.write('\\begin{tabular}{|c|c|c|}\n')
output_file_tex.write('\hline\n')
output_file_tex.write('Process & $\PWpm\PGg\PGg\\to\Pe\PGne\PGg\PGg$ & $\PWpm\PGg\PGg\\to\PGm\PGnGm\PGg\PGg$\\\\\n')
output_file_tex.write('\hline\n')
output_file_tex.write('data & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_data_obs[0][0], nevt_data_obs[1][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('expected signal & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_diboson[0][0], nevt_diboson[1][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('$\mathrm{{j}}\\to\PGg$ misid. & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_bkg_jetpho_misid[0][0], nevt_bkg_jetpho_misid[1][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('other irreducible + $\PW\PGg$ & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_bkg_irred[0][0], nevt_bkg_irred[1][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('$\PZ\PGg$ & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_bkg_egmisid[0][0], nevt_bkg_egmisid[1][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('\end{tabular}\n')
output_file_tex.write('\caption{Summary of the observed and predicted number of events with the full Run II statistics for the $\PW\PGg\PGg$ selection in the electron and muon channels.}\n')
output_file_tex.write('\label{t_wgg_evt}\n')
output_file_tex.write('\end{table}\n')
output_file_tex.write(' \n')
output_file_tex.write('\\begin{table}\n')
output_file_tex.write('\centering\n')
output_file_tex.write('\\begin{tabular}{|c|c|c|}\n')
output_file_tex.write('\hline\n')
output_file_tex.write('Process & $\PZ\PGg\PGg\\to\Pe\Pe\PGg\PGg$ & $\PZ\PGg\PGg\\to\PGm\PGm\PGg\PGg$\\\\\n')
output_file_tex.write('\hline\n')
output_file_tex.write('data & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_data_obs[2][0], nevt_data_obs[3][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('expected signal & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_diboson[2][0], nevt_diboson[3][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('$\mathrm{{j}}\\to\PGg$ misid. & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_bkg_jetpho_misid[2][0], nevt_bkg_jetpho_misid[3][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('other irreducible + $\PW\PGg$ & {0:.2f} & {1:.2f} \\\\\n'.format(nevt_bkg_irred[2][0], nevt_bkg_irred[3][0]))
output_file_tex.write('\hline\n')
output_file_tex.write('\end{tabular}\n')
output_file_tex.write('\caption{Summary of the observed and predicted number of events with the full Run II statistics for the $\PZ\PGg\PGg$ selection in the electron and muon channels.}\n')
output_file_tex.write('\label{t_zgg_evt}\n')
output_file_tex.write('\end{table}\n')

output_file_tex.close()
