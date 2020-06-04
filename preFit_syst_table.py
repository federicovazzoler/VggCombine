# To rework the dictionary logic
# following https://stackoverflow.com/questions/27118687/updating-nested-dictionaries-when-data-has-existing-key
#import collections
import sys
import os
import math
import ROOT

def fillSystForBosonChannel(syst, boson, channel, year, syst_dic):

  input_file = ROOT.TFile('cards/' + boson + '_' + channel + '_' + year + '.root')

  nevt_diboson          = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)] #[evt, stat, systUp, systDown]
  nevt_bkg_jetpho_misid = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)]
  nevt_bkg_egmisid      = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)]
  nevt_bkg_irred        = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)]
  nevt_sum_mc_tot       = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)]
  nevt_sum_mc_bkg       = [ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)]

  nevt_diboson[0] = input_file.Get('diboson').IntegralAndError(0, input_file.Get('diboson').GetNbinsX()+1, nevt_diboson[1])
  nevt_diboson[2] = input_file.Get('diboson_' + syst + 'Up').Integral(0, input_file.Get('diboson_' + syst + 'Up').GetNbinsX())
  nevt_diboson[3] = input_file.Get('diboson_' + syst + 'Down').Integral(0, input_file.Get('diboson_' + syst + 'Down').GetNbinsX())

  nevt_bkg_jetpho_misid[0] = input_file.Get('bkg_jetpho_misid').IntegralAndError(0, input_file.Get('bkg_jetpho_misid').GetNbinsX()+1, nevt_bkg_jetpho_misid[1])
  nevt_bkg_jetpho_misid[2] = input_file.Get('bkg_jetpho_misid_' + syst + 'Up').Integral(0, input_file.Get('bkg_jetpho_misid_' + syst + 'Up').GetNbinsX())
  nevt_bkg_jetpho_misid[3] = input_file.Get('bkg_jetpho_misid_' + syst + 'Down').Integral(0, input_file.Get('bkg_jetpho_misid_' + syst + 'Down').GetNbinsX())

  if boson == 'WGG':
    nevt_bkg_egmisid[0] = input_file.Get('bkg_egmisid').IntegralAndError(0, input_file.Get('bkg_egmisid').GetNbinsX()+1, nevt_bkg_egmisid[1])
    nevt_bkg_egmisid[2] = input_file.Get('bkg_egmisid_' + syst + 'Up').Integral(0, input_file.Get('bkg_egmisid_' + syst + 'Up').GetNbinsX())
    nevt_bkg_egmisid[3] = input_file.Get('bkg_egmisid_' + syst + 'Down').Integral(0, input_file.Get('bkg_egmisid_' + syst + 'Down').GetNbinsX())

  nevt_bkg_irred[0] = input_file.Get('bkg_irred').IntegralAndError(0, input_file.Get('bkg_irred').GetNbinsX()+1, nevt_bkg_irred[1])
  nevt_bkg_irred[2] = input_file.Get('bkg_irred_' + syst + 'Up').Integral(0, input_file.Get('bkg_irred_' + syst + 'Up').GetNbinsX())
  nevt_bkg_irred[3] = input_file.Get('bkg_irred_' + syst + 'Down').Integral(0, input_file.Get('bkg_irred_' + syst + 'Down').GetNbinsX())

  # systUp
  nevt_sum_mc_tot[0] = nevt_diboson[2] + nevt_bkg_jetpho_misid[2] + nevt_bkg_egmisid[2] + nevt_bkg_irred[2]
  nevt_sum_mc_tot[0] = nevt_sum_mc_tot[0] - (nevt_diboson[0] + nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])
  nevt_sum_mc_tot[0] = nevt_sum_mc_tot[0] / (nevt_diboson[0] + nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  #systDown
  nevt_sum_mc_tot[1] = nevt_diboson[3] + nevt_bkg_jetpho_misid[3] + nevt_bkg_egmisid[3] + nevt_bkg_irred[3]
  nevt_sum_mc_tot[1] = (nevt_diboson[0] + nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0]) - nevt_sum_mc_tot[1]
  nevt_sum_mc_tot[1] = nevt_sum_mc_tot[1] / (nevt_diboson[0] + nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  #stat
  nevt_sum_mc_tot[2] = nevt_diboson[1] + nevt_bkg_jetpho_misid[1] + nevt_bkg_egmisid[1] + nevt_bkg_irred[1]
  nevt_sum_mc_tot[2] = nevt_sum_mc_tot[2] / (nevt_diboson[0] + nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  # systUp
  nevt_sum_mc_bkg[0] = nevt_bkg_jetpho_misid[2] + nevt_bkg_egmisid[2] + nevt_bkg_irred[2]
  nevt_sum_mc_bkg[0] = nevt_sum_mc_bkg[0] - (nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])
  nevt_sum_mc_bkg[0] = nevt_sum_mc_bkg[0] / (nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  #systDown
  nevt_sum_mc_bkg[1] = nevt_bkg_jetpho_misid[3] + nevt_bkg_egmisid[3] + nevt_bkg_irred[3]
  nevt_sum_mc_bkg[1] = (nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0]) - nevt_sum_mc_bkg[1]
  nevt_sum_mc_bkg[1] = nevt_sum_mc_bkg[1] / (nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  #stat
  nevt_sum_mc_bkg[2] = nevt_bkg_jetpho_misid[1] + nevt_bkg_egmisid[1] + nevt_bkg_irred[1]
  nevt_sum_mc_bkg[2] = nevt_sum_mc_bkg[2] / (nevt_bkg_jetpho_misid[0] + nevt_bkg_egmisid[0] + nevt_bkg_irred[0])

  single_syst_dic = { syst : {
                        'sum_mc_tot' : {
                          'systUp' : nevt_sum_mc_tot[0],
                          'systDown' : nevt_sum_mc_tot[1],
                          'systAvg' : (abs(nevt_sum_mc_tot[0]) + abs(nevt_sum_mc_tot[1])) / 2.,
                          'stat' : nevt_sum_mc_tot[2],
                        },
                        'sum_mc_bkg' : {
                          'systUp' : nevt_sum_mc_bkg[0],
                          'systDown' : nevt_sum_mc_bkg[1],
                          'systAvg' : (abs(nevt_sum_mc_bkg[0]) + abs(nevt_sum_mc_bkg[1])) / 2.,
                          'stat' : nevt_sum_mc_bkg[2],
                        }
                      }
                    }

  return syst_dic.update(single_syst_dic)

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

folder = sys.argv[1]
folder += '/'
year = sys.argv[2]
syst_list = sys.argv[3].split(' ')
syst_list.remove('reference')
syst_list.remove('')

#syst_list = ['pileup', 'sf_ele_eff', 'sf_ele_reco', 'sf_ele_trig', 'sf_muo_id', 'sf_muo_iso', 'sf_muo_trig', 'sf_pho_eff', 'sf_pho_veto', 'l1prefiring', 'eg_misid', 'jet_misid']

syst_dic_WGG_ch_ele = {}
syst_dic_WGG_ch_muo = {}
syst_dic_ZGG_ch_ele = {}
syst_dic_ZGG_ch_muo = {}

for syst in syst_list:
  fillSystForBosonChannel(syst, 'WGG', 'ch_ele', year, syst_dic_WGG_ch_ele)
  fillSystForBosonChannel(syst, 'WGG', 'ch_muo', year, syst_dic_WGG_ch_muo)
  fillSystForBosonChannel(syst, 'ZGG', 'ch_ele', year, syst_dic_ZGG_ch_ele)
  fillSystForBosonChannel(syst, 'ZGG', 'ch_muo', year, syst_dic_ZGG_ch_muo)

output_file  = open(folder + 'preFit_syst_table_' + year + '.txt','w')

table_header = [' Syst', '| WGG ele (%) ', '| WGG muo (%) ', '| ZGG ele (%) ', '| ZGG muo (%) ']
table_row = ['' for i in range(len(syst_list) + 2)]

cell_w_syst = 15
cell_w = len(table_header[1])

i = 0
for syst in syst_list:
  table_row[i] += ' ' + syst
  for sp in range(cell_w_syst - len(table_row[i])):
    table_row[i] += ' '

  table_row[i] += '| {0:.2f}'.format(syst_dic_WGG_ch_ele.get(syst).get('sum_mc_bkg').get('systAvg') * 100)
  for sp in range(cell_w - 7):
    table_row[i] += ' '

  table_row[i] += '| {0:.2f}'.format(syst_dic_WGG_ch_muo.get(syst).get('sum_mc_bkg').get('systAvg') * 100)
  for sp in range(cell_w - 7):
    table_row[i] += ' '

  table_row[i] += '| {0:.2f}'.format(syst_dic_ZGG_ch_ele.get(syst).get('sum_mc_bkg').get('systAvg') * 100)
  for sp in range(cell_w - 7):
    table_row[i] += ' '

  table_row[i] += '| {0:.2f}'.format(syst_dic_ZGG_ch_muo.get(syst).get('sum_mc_bkg').get('systAvg') * 100)
  for sp in range(cell_w - 7):
    table_row[i] += ' '

  i += 1

lumi_list = [0.025, 0.023, 0.025, 0.018]
if year == '2016':
  lumi = lumi_list[0]
if year == '2017':
  lumi = lumi_list[1]
if year == '2018':
  lumi = lumi_list[2]
if year == 'Run2':
  lumi = lumi_list[3]

table_row[i] += ' lumi'
for sp in range(cell_w_syst - len(table_row[i])):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(lumi * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(lumi * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(lumi * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(lumi * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

i += 1

table_row[i] += ' mc stat'
for sp in range(cell_w_syst - len(table_row[i])):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(syst_dic_WGG_ch_ele.get(syst).get('sum_mc_bkg').get('stat') * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(syst_dic_WGG_ch_muo.get(syst).get('sum_mc_bkg').get('stat') * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(syst_dic_ZGG_ch_ele.get(syst).get('sum_mc_bkg').get('stat') * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '

table_row[i] += '| {0:.2f}'.format(syst_dic_ZGG_ch_muo.get(syst).get('sum_mc_bkg').get('stat') * 100)
for sp in range(cell_w - 7):
  table_row[i] += ' '


for i in range(len(table_header)):
  if i == 0:
    for sp in range(cell_w_syst - len(table_header[i])):
      table_header[i] += ' '
  else:
    for sp in range(cell_w - len(table_header[i])):
      table_header[i] += ' '

# output in table style
for i in range(len(table_row[0])):
  output_file.write('-')
output_file.write('\n')

for i in range(len(table_header)):
  output_file.write(table_header[i])
output_file.write('\n')

for i in range(len(table_row[0])):
  output_file.write('-')
output_file.write('\n')

for i in range(len(syst_list) + 2):
  output_file.write(table_row[i] + '\n')
  for j in range(len(table_row[0])):
    output_file.write('-')
  output_file.write('\n')

output_file.close()

# output in latex style
if year == 'Run2':
  output_file_latex = open(folder + 'preFit_syst_table_' + year + '_LATEX.txt','w')

  output_file_latex.write('\\begin{table}[ht]\n')
  output_file_latex.write('\centering\n')
  output_file_latex.write('\\begin{tabular}{|c|c|c|}\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('Systematic source & $\PW(\Pe\PGn)\PGg\PGg~(\%)$ & $\PW(\PGm\PGn)\PGg\PGg~(\%)$\\\\\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('Luminosity & {0:.2f} & {1:.2f}\\\\\n'.format(lumi * 100, lumi * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Pile-up & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('pileup').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('pileup').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
#  output_file_latex.write('Jet energy correction & $<1$ & $<1$\\\\\n')
#  output_file_latex.write('Jet energy resolution & $<1$ & $<1$\\\\\n')
#  output_file_latex.write('\hline\n')
  output_file_latex.write('Electron ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_ele_eff').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_ele_eff').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron reconstruction & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_ele_reco').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_ele_reco').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron trigger & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_ele_trig').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_ele_trig').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Muon ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_muo_id').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_muo_id').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Muon isolation & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_muo_iso').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_muo_iso').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Muon trigger & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_muo_trig').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_muo_trig').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Photon ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_pho_eff').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_pho_eff').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Photon pixel seed veto & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_pho_veto').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('sf_pho_veto').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('L1 ECAL trigger prefiring & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('l1prefiring').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('l1prefiring').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Jet-photon misid. & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('jet_misid').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('jet_misid').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron-photon misid. & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('eg_misid').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_WGG_ch_muo.get('eg_misid').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('MC samples statistical uncertainty & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_WGG_ch_ele.get('sf_ele_eff').get('sum_mc_bkg').get('stat') * 100, syst_dic_WGG_ch_muo.get('sf_ele_eff').get('sum_mc_bkg').get('stat') * 100))
  output_file_latex.write('Theoretical cross sections uncertainty & XXX & XXX\\\\\n')
  output_file_latex.write('%\hline\n')
  output_file_latex.write('%PDF sets & XXX & XXX\\\\\n')
  output_file_latex.write('%Scales ($\mu_F$, $\mu_R$) & XXX & XXX\\\\\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('\end{tabular}\n')
  output_file_latex.write('\caption{Summary of the pre-fit impact of every systematic uncertainty on the predicted number of background events for the $\PW\PGg\PGg$ measurement.}\n')
  output_file_latex.write('\label{t_systImp_prefit_wgg}\n')
  output_file_latex.write('\end{table}\n')
  output_file_latex.write('\n')
  output_file_latex.write('\\begin{table}[ht]\n')
  output_file_latex.write('\centering\n')
  output_file_latex.write('\\begin{tabular}{|c|c|c|}\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('Systematic source & $\PZ(\Pe\Pe)\PGg\PGg~(\%)$ & $\PZ(\PGm\PGm)\PGg\PGg~(\%)$\\\\\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('Luminosity & {0:.2f} & {1:.2f}\\\\\n'.format(lumi * 100, lumi * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Pile-up & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('pileup').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('pileup').get('sum_mc_bkg').get('systAvg') * 100))
#  output_file_latex.write('\hline\n')
#  output_file_latex.write('Jet energy correction & $<1$ & $<1$\\\\\n')
#  output_file_latex.write('Jet energy resolution & $<1$ & $<1$\\\\\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('Electron ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_ele_eff').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_ele_eff').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron reconstruction & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_ele_reco').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_ele_reco').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron trigger & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_ele_trig').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_ele_trig').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Muon ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_muo_id').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_muo_id').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Muon isolation & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_muo_iso').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_muo_iso').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Muon trigger & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_muo_trig').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_muo_trig').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Photon ID & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_pho_eff').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_pho_eff').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Photon pixel seed veto & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_pho_veto').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('sf_pho_veto').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('L1 ECAL trigger prefiring & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('l1prefiring').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('l1prefiring').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('Jet-photon misid. & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('jet_misid').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('jet_misid').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('Electron-photon misid. & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('eg_misid').get('sum_mc_bkg').get('systAvg') * 100, syst_dic_ZGG_ch_muo.get('eg_misid').get('sum_mc_bkg').get('systAvg') * 100))
  output_file_latex.write('\hline\n')
  output_file_latex.write('MC samples statistical uncertainty & {0:.2f} & {1:.2f}\\\\\n'.format(syst_dic_ZGG_ch_ele.get('sf_ele_eff').get('sum_mc_bkg').get('stat') * 100, syst_dic_ZGG_ch_muo.get('sf_ele_eff').get('sum_mc_bkg').get('stat') * 100))
  output_file_latex.write('Theoretical cross sections uncertainty & XXX & XXX\\\\\n')
  output_file_latex.write('%\hline\n')
  output_file_latex.write('%PDF sets & XXX & XXX\\\\\n')
  output_file_latex.write('%Scales ($\mu_F$, $\mu_R$) & XXX & XXX\\\\\n')
  output_file_latex.write('\hline\n')
  output_file_latex.write('\end{tabular}\n')
  output_file_latex.write('\caption{Summary of the pre-fit impact of every systematic uncertainty on the predicted number of background events for the $\PZ\PGg\PGg$ measurement.}\n')
  output_file_latex.write('\label{t_systImp_prefit_zgg}\n')
  output_file_latex.write('\end{table}\n')
