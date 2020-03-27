#!/bin/bash

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/FitDiagnostic/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
rm ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
rm ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind.root
rm ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.root
rm higgsCombineTest.FitDiagnostics*
rm combine_logger.out

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

#run fit diagnostic blinded (fixed signal strenght = 1)
combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal 1 -v 2 > ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind.txt
mv fitDiagnostics.root ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind.root
mv ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind.txt ${FOLDER}

#plot prefit
python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind ${CHANNEL} prefit ${FOLDER} blind

#plot postfit
python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind ${CHANNEL} postfit ${FOLDER} blind

#run fit diagnostic unblinded
combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 -v 3 --cminDefaultMinimizerType Minuit --cminDefaultMinimizerAlgo Scan > ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.txt
mv fitDiagnostics.root ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.root

mv ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.txt ${FOLDER}

#plot prefit
python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} prefit ${FOLDER}

#plot postfit
python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} postfit ${FOLDER}
