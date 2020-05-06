#!/bin/bash
URL_xsec="https://wwwusers.ts.infn.it/~dellaric/tmp/Vgg/v14.newgen5.default"
URL_pdf_scale="https://wwwusers.ts.infn.it/~gsorrent/FedericoVGG/25APR"

BOSON=$1
CHANNEL=$2
YEAR=$3

FOLDER="../html/combine_plots/likelihood_scan/SignalStrength/${BOSON}_${CHANNEL}_${YEAR}"
mkdir -p ${FOLDER}
rm ${FOLDER}/*

# fetch xsec from farmts
echo "Downloading theoretical xsec from : ${URL_xsec}"
wget -q -O ${BOSON}_${CHANNEL}_${YEAR}_theoxsec.txt ${URL_xsec}/reference/${YEAR}.xsec/root/h_${BOSON}_${CHANNEL:3}_pho0_pho1_pt.dat

echo "Downloading pdf and scale file from : ${URL_pdf_scale}"
wget -q -O ${BOSON}_PDF.txt ${URL_pdf_scale}/${BOSON}_PDF.txt

rMin=-1
rMax=4
nPoints=1000

# build workspace
rm ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
text2workspace.py ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt  -o ${BOSON}_${CHANNEL}_${YEAR}_workspace.root
cp ../cards/${BOSON}_${CHANNEL}_${YEAR}_datacard.txt ${FOLDER} 

# BLIND
python automatedSignalStrength.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root ${rMin} ${rMax} ${nPoints} blind

python plot1DScan.py higgsCombineTest.MultiDimFit.mH200.root --others 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' -o ${BOSON}_${CHANNEL}_${YEAR}_signalstrength --breakdown Syst,Stat
cp ${BOSON}_${CHANNEL}_${YEAR}_signalstrength.pdf ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_signalstrength_blind.pdf

python ExtractXsec4Paper.py ${BOSON} ${CHANNEL} ${YEAR} higgsCombineTest.MultiDimFit.mH200.root 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' blind ${URL_xsec}/reference/${YEAR}.xsec/root/h_${BOSON}_${CHANNEL:3}_pho0_pho1_pt.dat ${URL_pdf_scale}/${BOSON}_PDF.txt
cp ${BOSON}_${CHANNEL}_${YEAR}_xsec4paper_blind.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_xsec4paper_blind.txt

rm higgsCombine* *.out *.png *.pdf

# UNBLIND
python automatedSignalStrength.py ${BOSON}_${CHANNEL}_${YEAR}_workspace.root ${rMin} ${rMax} ${nPoints} unblind

python plot1DScan.py higgsCombineTest.MultiDimFit.mH200.root --others 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' -o ${BOSON}_${CHANNEL}_${YEAR}_signalstrength --breakdown Syst,Stat
cp ${BOSON}_${CHANNEL}_${YEAR}_signalstrength.pdf ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_signalstrength_unblind.pdf

python ExtractXsec4Paper.py ${BOSON} ${CHANNEL} ${YEAR} higgsCombineTest.MultiDimFit.mH200.root 'higgsCombine.freezeAll.MultiDimFit.mH200.root:FreezeAll:2' unblind ${URL_xsec}/reference/${YEAR}.xsec/root/h_${BOSON}_${CHANNEL:3}_pho0_pho1_pt.dat ${URL_pdf_scale}/${BOSON}_PDF.txt
cp ${BOSON}_${CHANNEL}_${YEAR}_xsec4paper_unblind.txt ${FOLDER}/${BOSON}_${CHANNEL}_${YEAR}_xsec4paper_unblind.txt

rm *.root *.out *.png *.pdf *.txt
