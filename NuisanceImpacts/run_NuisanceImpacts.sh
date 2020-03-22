#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/NuisanceImpacts/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}

#clean
rm ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
rm combine_logger.out
rm ${BOSON}_${CHANNEL}_${YEAR}_impacts.json
rm higgsCombine_initialFit_Test*
rm higgsCombine_paramFit_Test*
rm ${BOSON}_${CHANNEL}_${YEAR}_impacts.pdf

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

#initial fit of mu
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -10 --rMax 10 --robustFit 1 --doInitialFit

#fit separately every nuisance
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -10 --rMax 10 --robustFit 1 --doFits

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -10 --rMax 10 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result blind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind -t rename.json --blind
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind.pdf ${FOLDER}

#plot the result unblind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts.pdf ${FOLDER}
