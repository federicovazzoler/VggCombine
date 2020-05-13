#!/bin/bash

FOLDER=$1/syst_shape_plot
mkdir -p $FOLDER
BOSONS="WGG ZGG"
CHANNELS="ch_ele ch_muo"
YEARS="2016 2017 2018 Run2"

FLAGS=""
FLAGS=$FLAGS" reference"
FLAGS=$FLAGS" pileup"
#FLAGS=$FLAGS" jec"
#FLAGS=$FLAGS" jer"
FLAGS=$FLAGS" sf_ele_eff"
FLAGS=$FLAGS" sf_ele_reco"
FLAGS=$FLAGS" sf_ele_trig"
FLAGS=$FLAGS" sf_muo_id"
FLAGS=$FLAGS" sf_muo_iso"
FLAGS=$FLAGS" sf_muo_trig"
FLAGS=$FLAGS" sf_pho_eff"
FLAGS=$FLAGS" sf_pho_veto"
FLAGS=$FLAGS" l1prefiring"
FLAGS=$FLAGS" eg_misid"
FLAGS=$FLAGS" jet_misid"

for YEAR in ${YEARS}; do
  python number_of_events.py ${FOLDER} ${YEAR}
  python preFit_syst_table.py ${FOLDER} ${YEAR} "${FLAGS}"
  for BOSON in ${BOSONS}; do
    for CHANNEL in ${CHANNELS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      mkdir -p ${FOLDER}/${BOSON}/${CHANNEL}/${YEAR}
      for FLAG in ${FLAGS}; do
        if [[ "${FLAG}" != "reference" ]]; then
          echo "--- ${FLAG}"
          python plotSyst.py ${FOLDER} ${BOSON} ${CHANNEL} ${YEAR} ${FLAG}
        fi
      done
      echo ""
    done
  done
done
