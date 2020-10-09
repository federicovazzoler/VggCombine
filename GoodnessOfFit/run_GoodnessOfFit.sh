#!/bin/bash

FOLDER=$1
BOSON=$2
CHANNEL=$3
YEAR=$4
FOLDER=$FOLDER/${BOSON}_${CHANNEL}_${YEAR}
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out" -o -name "*.txt" -o -name "*.pdf")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

nTOYS=500

cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER}

#run first time on actual data to obtain t_0
combine -M GoodnessOfFit ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt --algo=saturated
mv higgsCombineTest.GoodnessOfFit.mH120.root ${BOSON}_${CHANNEL}_${YEAR}_GoodnessOfFit.root

#generate toy to infer t distribution
combine -M GoodnessOfFit ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt --algo=saturated -t ${nTOYS} -s -1 --toysFreq
mv higgsCombineTest.GoodnessOfFit.mH120*.root ${BOSON}_${CHANNEL}_${YEAR}_GoodnessOfFit_toys.root

#p-value
#python p_value.py ${BOSON} ${CHANNEL} ${YEAR} ${nTOYS}
python plotGOF.py ${BOSON} ${CHANNEL} ${YEAR} ${nTOYS}
cp ${BOSON}_${CHANNEL}_${YEAR}_p_value.txt ${FOLDER}/
cp ${BOSON}_${CHANNEL}_${YEAR}_p_value.pdf ${FOLDER}/
