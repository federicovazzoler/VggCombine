#!/bin/bash

FOLDER=$1/likelihood_scan/NuisanceImpacts
mkdir -p $FOLDER
BOSONS="WGG ZGG"
CHANNELS="ch_ele ch_muo ch_lep"
#YEARS="2016 2017 2018 Run2"
YEARS="Run2"

for BOSON in ${BOSONS}; do
  for CHANNEL in ${CHANNELS}; do
    for YEAR in ${YEARS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      ./run_NuisanceImpacts.sh ${FOLDER} ${BOSON} ${CHANNEL} ${YEAR}
      FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out" -o -name "*.txt" -o -name "*.pdf" -o -name "*impacts.json")
      if [[ "${FILETOREMOVE}" != "" ]]; then
        rm -v ${FILETOREMOVE}
      fi
      echo ""
    done
  done
done
