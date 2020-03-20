#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/SignalStrength/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}

#clean
rm higgsCombine* *.pdf *.png

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

# signal strenght
combine -M MultiDimFit ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -1 --rMax 10 --algo grid --points 1000 --robustFit=1

combine -M MultiDimFit ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -n .snapshot -m 200 --rMin -1 --rMax 10 --saveWorkspace --robustFit=1

combine -M MultiDimFit higgsCombine.snapshot.MultiDimFit.mH200.root -n .freezeAll -m 200 --rMin -1 --rMax 10 --algo grid --points 1000 --freezeParameters pileup,jec,jer,sf_ele_eff,sf_ele_reco,sf_ele_trig,sf_muo_id,sf_muo_iso,sf_muo_trig,sf_pho_eff,sf_pho_veto,l1prefiring,eg_misid,jet_misid --snapshotName MultiDimFit --robustFit=1

python plot1DScan.py higgsCombineTest.MultiDimFit.mH200.root --others 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' -o ${BOSON}_${CHANNEL}_${YEAR}_signalstrength --breakdown Syst,Stat
cp ${BOSON}_${CHANNEL}_${YEAR}_signalstrength.pdf ${FOLDER}
