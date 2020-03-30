#!/bin/bash

./run_all_shapes.sh

cd cards
./combine_channels.sh
cd ..

cd DatacardValidation
./run_DatacardValidation.sh
cd ..

cd FitDiagnostics
./run_all.sh
cd ..

cd GoodnessOfFit
./run_all.sh
cd ..

cd NuisanceImpacts
./run_all.sh
cd ..

cd SignalStrength
./run_all.sh
cd ..

cd Significance
./run_all.sh
cd ..
