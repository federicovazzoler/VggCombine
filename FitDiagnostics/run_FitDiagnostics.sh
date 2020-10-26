#!/bin/bash

FOLDER=$1
BOSON=$2
CHANNEL=$3
YEAR=$4
FOLDER=$FOLDER/${BOSON}_${CHANNEL}_${YEAR}
mkdir -p ${FOLDER}
rm ${FOLDER}/*

#clean
FILETOREMOVE=$(find ./ -name "*.root" -o -name "*.out")
if [[ "${FILETOREMOVE}" != "" ]]; then
  rm -v ${FILETOREMOVE}
fi

#build workspace
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER}

echo ""
echo "run fit diagnostic blinded (fixed signal strenght = 0)"
echo ""
combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal 0 -v 2 --minos=all > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0.txt
mv fitDiagnostics.root ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0.root

#diffNuisances plot
python diffNuisances.py -A -a ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0.root -g ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0_plots.root > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_diffNuisances_blind_mu0.txt

python PlotDiffNuisances.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0_plots ${FOLDER}

if [[ "${CHANNEL}" != "ch_lep" ]]; then
  #plot prefit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0 ${CHANNEL} prefit ${FOLDER} blind_mu0

  #plot postfit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu0 ${CHANNEL} postfit ${FOLDER} blind_mu0
fi

echo ""
echo "run fit diagnostic blinded (fixed signal strenght = 1)"
echo ""
combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal 1 -v 2 --minos=all > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1.txt
mv fitDiagnostics.root ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1.root

#diffNuisances plot
python diffNuisances.py -A -a ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1.root -g ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1_plots.root > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_diffNuisances_blind_mu1.txt

python PlotDiffNuisances.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1_plots ${FOLDER}

if [[ "${CHANNEL}" != "ch_lep" ]]; then
  #plot prefit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1 ${CHANNEL} prefit ${FOLDER} blind_mu1

  #plot postfit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_blind_mu1 ${CHANNEL} postfit ${FOLDER} blind_mu1
fi

echo ""
echo "run fit diagnostic unblinded"
echo ""
#combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 -v 3 --cminDefaultMinimizerType Minuit --cminDefaultMinimizerAlgo Scan --minos=all > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.txt
combine -M FitDiagnostics ${BOSON}_${CHANNEL}_${YEAR}_workspace.root -m 125 --rMin -2 --rMax 2 --saveShapes --saveWithUncertainties -v 3 --minos=all > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.txt
mv fitDiagnostics.root ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.root

#diffNuisances plot
python diffNuisances.py -A -a ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.root -g ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_plots.root > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_diffNuisances.txt

python PlotDiffNuisances.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic_plots ${FOLDER}

if [[ "${CHANNEL}" != "ch_lep" ]]; then
  #plot prefit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} prefit ${FOLDER}
  python FitPlot_v2.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} prefit ${FOLDER}

  #plot postfit
  python FitPlot.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} postfit ${FOLDER}
  python FitPlot_v2.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic ${CHANNEL} postfit ${FOLDER}
 
  python mlfitNormsToText.py ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic.root -u > ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_nevt.txt

  python FitPlot_v3.py -input_file ${BOSON}_${CHANNEL}_${YEAR}_fitDiagnostic -channel ${CHANNEL} -output_folder ${FOLDER}
fi
