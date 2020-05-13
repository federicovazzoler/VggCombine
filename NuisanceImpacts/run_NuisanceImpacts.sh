#!/bin/bash

FOLDER=$1
BOSON=$2
CHANNEL=$3
YEAR=$4
FOLDER=${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out" -o -name "*.txt" -o -name "*.pdf" -o -name "*impacts.json")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER}

#+++++BLIND mu = 0+++++
python looTcombine.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -4 4 0

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -4 --rMax 4 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result blind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind_mu0 -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind_mu0.pdf ${FOLDER}

#extract uncertainties blind
python ExtractNuisance4Paper.py ${BOSON} ${CHANNEL} ${YEAR}
cp ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_syst_unc_blind_mu0.txt

#clean before rerunnig
FILETOREMOVE=$(find ./ -name "higgsCombine*" -o -name "*.out" -o -name "*.txt" -o -name "*.pdf" -o -name "*impacts.json")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

#+++++BLIND mu = 1+++++
python looTcombine.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -4 4 1

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -4 --rMax 4 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result blind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind_mu1 -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts_blind_mu1.pdf ${FOLDER}

#extract uncertainties blind
python ExtractNuisance4Paper.py ${BOSON} ${CHANNEL} ${YEAR}
cp ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_syst_unc_blind_mu1.txt

#clean before rerunnig
FILETOREMOVE=$(find ./ -name "higgsCombine*" -o -name "*.out" -o -name "*.txt" -o -name "*.pdf" -o -name "*impacts.json")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

#+++++UNBLIND+++++
#initial fit of mu
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -4 --rMax 4 --robustFit 1 --doInitialFit

#fit separately every nuisance
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -4 --rMax 4 --robustFit 1 --doFits

#collect output and convert to json file
combineTool.py -M Impacts -d ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 200 --rMin -4 --rMax 4 --robustFit 1 --output ${BOSON}_${CHANNEL}_${YEAR}_impacts.json

#plot the result unblind
plotImpacts.py -i ${BOSON}_${CHANNEL}_${YEAR}_impacts.json -o ${BOSON}_${CHANNEL}_${YEAR}_impacts -t rename.json
cp ${BOSON}_${CHANNEL}_${YEAR}_impacts.pdf ${FOLDER}

#extract uncertainties unblind
python ExtractNuisance4Paper.py ${BOSON} ${CHANNEL} ${YEAR}
cp ${BOSON}_${CHANNEL}_${YEAR}_syst_unc.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_syst_unc_unblind.txt
