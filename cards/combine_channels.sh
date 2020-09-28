#!/bin/bash

BOSONS="WGG ZGG"
#YEARS="2016 2017 2018 Run2"
YEARS="Run2"

for BOSON in ${BOSONS}; do
  for YEAR in ${YEARS}; do
    echo "Combining ch_ele and ch_muo for ${BOSON} in year ${YEAR}"
    combineCards.py ch_ele=${BOSON}_ch_ele_${YEAR}_datacard.txt ch_muo=${BOSON}_ch_muo_${YEAR}_datacard.txt > ${BOSON}_ch_lep_${YEAR}_datacard.txt
  done
done
