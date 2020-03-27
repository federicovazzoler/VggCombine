#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/SignalStrength/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}

rMin=-1
rMax=10
nPoints=1000

# build workspace
rm ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

# BLIND
python automatedSignalStrength.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root ${rMin} ${rMax} ${nPoints} blind

python plot1DScan.py higgsCombineTest.MultiDimFit.mH200.root --others 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' -o ${BOSON}_${CHANNEL}_${YEAR}_signalstrength --breakdown Syst,Stat
cp ${BOSON}_${CHANNEL}_${YEAR}_signalstrength.pdf ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_signalstrength_blind.pdf

rm higgsCombine* *.out *.png *.pdf

# UNBLIND
python automatedSignalStrength.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root ${rMin} ${rMax} ${nPoints} unblind

python plot1DScan.py higgsCombineTest.MultiDimFit.mH200.root --others 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' -o ${BOSON}_${CHANNEL}_${YEAR}_signalstrength --breakdown Syst,Stat
cp ${BOSON}_${CHANNEL}_${YEAR}_signalstrength.pdf ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_signalstrength_unblind.pdf

rm *.root *.out *.png *.pdf
