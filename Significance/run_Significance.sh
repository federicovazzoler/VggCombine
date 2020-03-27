#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/Significance/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
rm ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
rm ${BOSON}_${CHANNEL}_${YEAR}_significance_*

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER}

#significance: asymptotic
#expected
combine -M Significance ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -10 --rMax 10 -t -1 --expectSignal 1 > ${BOSON}_${CHANNEL}_${YEAR}_significance_expected.txt
mv higgsCombineTest.Significance.mH200.root ${BOSON}_${CHANNEL}_${YEAR}_significance_expected.root
cp ${BOSON}_${CHANNEL}_${YEAR}_significance_expected.txt ${FOLDER} 

#observed
combine -M Significance ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -10 --rMax 10 > ${BOSON}_${CHANNEL}_${YEAR}_significance_observed.txt
mv higgsCombineTest.Significance.mH200.root ${BOSON}_${CHANNEL}_${YEAR}_significance_observed.root
cp ${BOSON}_${CHANNEL}_${YEAR}_significance_observed.txt ${FOLDER} 
