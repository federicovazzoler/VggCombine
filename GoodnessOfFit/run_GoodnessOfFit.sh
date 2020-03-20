#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/GoodnessOfFit/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}

#clean
rm *.root
rm combine_logger.out
rm ${FOLDER}/*.txt

nTOYS=500

cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

#run first time on actual data to obtain t_0
combine -M GoodnessOfFit ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt --algo=saturated
mv higgsCombineTest.GoodnessOfFit.mH120.root ${BOSON}_${CHANNEL}_${YEAR}_GoodnessOfFit.root

#generate toy to infer t distribution
combine -M GoodnessOfFit ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt --algo=saturated -t ${nTOYS} -s -1
mv higgsCombineTest.GoodnessOfFit.mH120*.root ${BOSON}_${CHANNEL}_${YEAR}_GoodnessOfFit_toys.root

#p-value
python p_value.py ${BOSON} ${CHANNEL} ${YEAR} ${nTOYS} 
cp ${BOSON}_${CHANNEL}_${YEAR}_p_value.txt ${FOLDER}/
