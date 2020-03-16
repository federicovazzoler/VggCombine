#!/bin/bash

BOSONS="WGG ZGG"

CHANNELS="ch_ele ch_muo"

YEARS="2016 2017 2018 Run2"

for BOSON in ${BOSONS}; do
  for CHANNEL in ${CHANNELS}; do
    for YEAR in ${YEARS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      ./run_SignalStrength.sh ${BOSON} ${CHANNEL} ${YEAR}
      rm *.root *.out *.pdf
      echo ""
    done
  done
done