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
rm ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt
rm ${FOLDER}/*

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

#BLIND
python looTcombine.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root 0 4

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin 0 --rMax 4 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result blind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind.pdf ${FOLDER}

#extract uncertainties blind
python ExtractNuisance4Paper.py ${BOSON} ${CHANNEL} ${YEAR}
cp ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_syst_unc_blind.txt

#clean before rerunnig for unblind
rm combine_logger.out
rm ${BOSON}_${CHANNEL}_${YEAR}_impacts.json
rm higgsCombine_initialFit_Test*
rm higgsCombine_paramFit_Test*
rm ${BOSON}_${CHANNEL}_${YEAR}_impacts.pdf
rm ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt

#UNBLIND
#initial fit of mu
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin 0 --rMax 4 --robustFit 1 --doInitialFit

#fit separately every nuisance
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin 0 --rMax 4 --robustFit 1 --doFits

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin 0 --rMax 4 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result unblind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts.pdf ${FOLDER}

#extract uncertainties unblind
python ExtractNuisance4Paper.py ${BOSON} ${CHANNEL} ${YEAR}
cp ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_syst_unc_unblind.txt
