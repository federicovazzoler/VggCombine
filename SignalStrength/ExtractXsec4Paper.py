#!/usr/bin/env python

import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path
import os
import sys

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle(width=700, l=0.13)
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetMarkerSize(0.7)

NAMECOUNTER = 0

def read(scan, param, files, ycut):
    goodfiles = [f for f in files if plot.TFileIsGood(f)]
    limit = plot.MakeTChain(goodfiles, 'limit')
    graph = plot.TGraphFromTree(limit, param, '2*deltaNLL', 'quantileExpected > -1.5')
    graph.SetName(scan)
    graph.Sort()
    plot.RemoveGraphXDuplicates(graph)
    plot.RemoveGraphYAbove(graph, ycut)
    # graph.Print()
    return graph


def Eval(obj, x, params):
    return obj.Eval(x[0])


def BuildScan(scan, param, files, color, yvals, ycut):
    graph = read(scan, param, files, ycut)
    bestfit = None
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] == 0.:
            bestfit = graph.GetX()[i]
    graph.SetMarkerColor(color)
    spline = ROOT.TSpline3("spline3", graph)
    global NAMECOUNTER
    func = ROOT.TF1('splinefn'+str(NAMECOUNTER), partial(Eval, spline), graph.GetX()[0], graph.GetX()[graph.GetN() - 1], 1)
    NAMECOUNTER += 1
    func.SetLineColor(color)
    func.SetLineWidth(3)
    assert(bestfit is not None)
    crossings = {}
    cross_1sig = None
    cross_2sig = None
    other_1sig = []
    other_2sig = []
    val = None
    val_2sig = None
    for yval in yvals:
        crossings[yval] = plot.FindCrossingsWithSpline(graph, func, yval)
        for cr in crossings[yval]:
            cr["contains_bf"] = cr["lo"] <= bestfit and cr["hi"] >= bestfit
    for cr in crossings[yvals[0]]:
        if cr['contains_bf']:
            val = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
            cross_1sig = cr
        else:
            other_1sig.append(cr)
    if len(yvals) > 1:
        for cr in crossings[yvals[1]]:
            if cr['contains_bf']:
                val_2sig = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
                cross_2sig = cr
            else:
                other_2sig.append(cr)
    else:
        val_2sig = (0., 0., 0.)
        cross_2sig = cross_1sig
    return {
        "graph"     : graph,
        "spline"    : spline,
        "func"      : func,
        "crossings" : crossings,
        "val"       : val,
        "val_2sig": val_2sig,
        "cross_1sig" : cross_1sig,
        "cross_2sig" : cross_2sig,
        "other_1sig" : other_1sig,
        "other_2sig" : other_2sig
    }

boson = sys.argv[1]
channel = sys.argv[2]
year = sys.argv[3]
input4buildscan = sys.argv[4] #higgsCombineTest.MultiDimFit.mH200.root
othersinput = [sys.argv[5]] #higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2
isBlind = sys.argv[6]

output4buildscan = boson + '_' + channel + '_' + year + '_signalstrength'
POI = 'r'
main_color = 1
yvals = [1., 4.]
y_cut = 7.

main_scan = BuildScan(output4buildscan, POI, [input4buildscan], main_color, yvals, y_cut)

other_scans = [ ]
other_scans_opts = [ ]
for oargs in othersinput:
  splitargs = oargs.split(':')
  other_scans_opts.append(splitargs)
  other_scans.append(BuildScan(output4buildscan, POI, [splitargs[0]], int(splitargs[2]), yvals, y_cut))

canv = ROOT.TCanvas(output4buildscan, output4buildscan)
pads = plot.OnePad()
main_scan['graph'].SetMarkerColor(1)
main_scan['graph'].Draw('AP')

axishist = plot.GetAxisHist(pads[0])

new_min = axishist.GetXaxis().GetXmin()
new_max = axishist.GetXaxis().GetXmax()
mins = []
maxs = []
for other in other_scans:
    mins.append(other['graph'].GetX()[0])
    maxs.append(other['graph'].GetX()[other['graph'].GetN()-1])

if len(other_scans) > 0:
    if min(mins) < main_scan['graph'].GetX()[0]:
        new_min = min(mins) - (main_scan['graph'].GetX()[0] - new_min)
    if max(maxs) > main_scan['graph'].GetX()[main_scan['graph'].GetN()-1]:
        new_max = max(maxs) + (new_max - main_scan['graph'].GetX()[main_scan['graph'].GetN()-1])
    axishist.GetXaxis().SetLimits(new_min, new_max)

crossings = main_scan['crossings']
val_nom = main_scan['val']
val_2sig = main_scan['val_2sig']
breakdown = 'Syst,Stat'

breakdown = breakdown.split(',')
v_hi = [val_nom[1]]
v_lo = [val_nom[2]]
for other in other_scans:
  v_hi.append(other['val'][1])
  v_lo.append(other['val'][2])
  assert(len(v_hi) == len(breakdown))
  mu = val_nom[0]
    
  #syst
  i = 0
  if (abs(v_hi[1]) > abs(v_hi[0])):
    print 'ERROR SUBTRACTION IS NEGATIVE FOR Syst HI'
    hi_syst = 0.
  else:
    hi_syst = math.sqrt(v_hi[0]*v_hi[0] - v_hi[1]*v_hi[1])
  if (abs(v_lo[1]) > abs(v_lo[0])):
    print 'ERROR SUBTRACTION IS NEGATIVE FOR Syst LO'
    lo_syst = 0.
  else:
    lo_syst = math.sqrt(v_lo[0]*v_lo[0] - v_lo[1]*v_lo[1])

  #stat
  hi_stat = v_hi[1]
  lo_stat = v_lo[1]

# open theo xsec
inputXsec = open(boson + '_' + channel + '_' + year + '_theoxsec.txt').readline().strip().split('(')[1].replace(')', '')

inputXsec = float(inputXsec) * 1000

combineXsec = float(inputXsec) * float(mu)
combineXsec_syst_hi = float(inputXsec) * float(hi_syst)
combineXsec_syst_lo = float(inputXsec) * float(lo_syst)
combineXsec_stat_hi = float(inputXsec) * float(hi_stat)
combineXsec_stat_lo = float(inputXsec) * float(lo_stat)

# output

output_file = open(boson + "_" + channel + "_" + year + "_xsec4paper" + "_" + isBlind + ".txt","w")

output_file.write('Mu = {0}\n'.format(mu))
output_file.write('Generator xsec = {0}\n'.format(inputXsec))
output_file.write('Combine xsec = {0:.2f} +{1:.2f} -{2:.2f} (Syst.) +{3:.2f} -{4:.2f} (Stat.)\n'.format(abs(combineXsec), abs(combineXsec_syst_hi), abs(combineXsec_syst_lo), abs(combineXsec_stat_hi), abs(combineXsec_stat_lo)))
output_file.write('\n')
output_file.write('Latex 4 paper : \n')
output_file.write('\n')

if boson == 'WGG':
  if channel == 'ch_ele':
    xsec_string = '\sigma(\PW\PGg\PGg)^\mathrm{{exp.}}_{{\Pe\PGn}} &= {0:.2f} '.format(combineXsec)
    syststat_string = '^{{{0:.2f}}}_{{{1:.2f}}} \mathrm{{(syst.)}} ^{{{2:.2f}}}_{{{3:.2f}}} \mathrm{{(stat.)}} '.format(abs(combineXsec_syst_hi), abs(combineXsec_syst_lo), abs(combineXsec_stat_hi), abs(combineXsec_stat_lo))
    if year == 'Run2':
      theo_string = '\pm 0.08 \mathrm{(theo)} '
    else:
      theo_string = ''
  elif channel == 'ch_muo':
    xsec_string = '\sigma(\PW\PGg\PGg)^\mathrm{{exp.}}_{{\PGm\PGn}} &= {0:.2f} '.format(combineXsec)
    syststat_string = '^{{{0:.2f}}}_{{{1:.2f}}} \mathrm{{(syst.)}} ^{{{2:.2f}}}_{{{3:.2f}}} \mathrm{{(stat.)}} '.format(abs(combineXsec_syst_hi), abs(combineXsec_syst_lo), abs(combineXsec_stat_hi), abs(combineXsec_stat_lo))
    if year == 'Run2':
      theo_string = '\pm 0.08 \mathrm{(theo)} '
    else:
      theo_string = ''
elif boson == 'ZGG':
  if channel == 'ch_ele':
    xsec_string = '\sigma(\PZ\PGg\PGg)^\mathrm{{exp.}}_{{\Pe\Pe}} &= {0:.2f} '.format(combineXsec)
    syststat_string = '^{{{0:.2f}}}_{{{1:.2f}}} \mathrm{{(syst.)}} ^{{{2:.2f}}}_{{{3:.2f}}} \mathrm{{(stat.)}} '.format(abs(combineXsec_syst_hi), abs(combineXsec_syst_lo), abs(combineXsec_stat_hi), abs(combineXsec_stat_lo))
    if year == 'Run2':
      theo_string = '\pm 0.05 \mathrm{(theo)} '
    else:
      theo_string = ''
  elif channel == 'ch_muo':
    xsec_string = '\sigma(\PZ\PGg\PGg)^\mathrm{{exp.}}_{{\PGm\PGm}} &= {0:.2f} '.format(combineXsec)
    syststat_string = '^{{{0:.2f}}}_{{{1:.2f}}} \mathrm{{(syst.)}} ^{{{2:.2f}}}_{{{3:.2f}}} \mathrm{{(stat.)}} '.format(abs(combineXsec_syst_hi), abs(combineXsec_syst_lo), abs(combineXsec_stat_hi), abs(combineXsec_stat_lo))
    if year == 'Run2':
      theo_string = '\pm 0.06 \mathrm{(theo)} '
    else:
      theo_string = ''

output_file.write(xsec_string + syststat_string + theo_string + '\, \mathrm{{fb}} \\' + '\\')

output_file.close()
