#!/bin/bash

FOLDER=$1/likelihood_scan/DatacardValidation
mkdir -p ${FOLDER}
rm ${FOLDER}/*

BOSONS="WGG ZGG"
CHANNELS="ch_ele ch_muo ch_lep"
YEARS="2016 2017 2018 Run2"

for BOSON in ${BOSONS}; do
  for YEAR in ${YEARS}; do
    for CHANNEL in ${CHANNELS}; do
      cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER}
      echo "--------------------------------------------------"
      echo "Validating datacard : ${BOSON}_${CHANNEL}_${YEAR}_datacard.txt"
      echo "--------------------------------------------------"
      ValidateDatacards.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt -p 3 --jsonFile ${BOSON}_${CHANNEL}_${YEAR}_datacard_validation.json > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_datacard_validation.txt
      echo ""
    done
  done
done

FILETOREMOVE=$(find ./ -name "*.txt" -o -name "*.json")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi
