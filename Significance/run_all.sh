#!/bin/bash

BOSONS="WGG ZGG"

CHANNELS="ch_ele ch_muo ch_lep"

YEARS="2016 2017 2018 Run2"

for BOSON in ${BOSONS}; do
  for CHANNEL in ${CHANNELS}; do
    for YEAR in ${YEARS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      ./run_Significance.sh ${BOSON} ${CHANNEL} ${YEAR}
      rm *.root *.out *.txt
      echo ""
    done
  done
done
