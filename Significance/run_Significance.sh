#!/bin/bash

FOLDER=$1
BOSON=$2
CHANNEL=$3
YEAR=$4
FOLDER=${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out" -o -name "*.txt")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
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
