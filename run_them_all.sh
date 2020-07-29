#!/bin/bash

eval `scramv1 runtime -sh`

if [[ $1 == "" ]]; then
  echo "please specify output folder"
  exit 1
fi

FOLDER=$(pwd)/html/combine/$1
mkdir -p $FOLDER

URL_xsec=https://wwwusers.ts.infn.it/~dellaric/tmp/Vgg/$1
URL_pdf_scale=https://wwwusers.ts.infn.it/~fvazzole/rivet/$1

url_string_xsec="Theoretical xsecs from : ${URL_xsec}"
url_string_theo="Theoretical uncs on xsec from : ${URL_pdf_scale}"
length=${#url_string_xsec}
length1=${#url_string_theo}
if [[ $length1 > $length ]]; then
  length=$length1
fi
echo ""
for (( c=0; c<${length}; c++ ))
do
  printf "*"
done
echo ""
echo "$url_string_xsec"
echo "$url_string_theo"
for (( c=0; c<${length}; c++ ))
do
  printf "*"
done
echo ""
echo ""

sleep 10

./run_all_shapes.sh $FOLDER
echo ""

cd cards
./combine_channels.sh
echo ""
cd ..

cd DatacardValidation
./run_DatacardValidation.sh $FOLDER
echo ""
cd ..

cd FitDiagnostics
./run_all.sh $FOLDER
echo ""
cd ..

cd GoodnessOfFit
./run_all.sh $FOLDER
echo ""
cd ..

cd NuisanceImpacts
./run_all.sh $FOLDER
echo ""
cd ..

cd SignalStrength
./run_all.sh $FOLDER $URL_xsec $URL_pdf_scale
echo ""
cd ..

cd Significance
./run_all.sh $FOLDER
echo ""
cd ..

./forRepository.sh $1

exit
