#!/bin/bash

FOLDER=$1/likelihood_scan/SignalStrength
mkdir -p $FOLDER
URL_xsec=$2
URL_pdf_scale=$3
BOSONS="WGG ZGG"
CHANNELS="ch_ele ch_muo ch_lep"
YEARS="2016 2017 2018 Run2"

for BOSON in ${BOSONS}; do
  for CHANNEL in ${CHANNELS}; do
    for YEAR in ${YEARS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      ./run_SignalStrength.sh ${FOLDER} ${BOSON} ${CHANNEL} ${YEAR} ${URL_xsec} ${URL_pdf_scale}
      rm *.root *.out *.pdf
      FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out" -o -name "*.pdf")
      if [[ "${FILETOREMOVE}" != "" ]]; then
        rm -v ${FILETOREMOVE}
      fi
      echo ""
    done
  done
done
