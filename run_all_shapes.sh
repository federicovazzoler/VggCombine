#!/bin/bash

mkdir -p html/combine_plots

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

for BOSON in ${BOSONS}; do
  for CHANNEL in ${CHANNELS}; do
    for YEAR in ${YEARS}; do
      echo "--- ${BOSON} - ${CHANNEL} - ${YEAR} ---"
      mkdir -p html/combine_plots/syst_shape_plot/${BOSON}/${CHANNEL}/${YEAR}
      for FLAG in ${FLAGS}; do
        echo "--- ${FLAG}"
        if [[ "${FLAG}" == "reference" ]]; then
          python number_of_events.py ${YEAR}
          mv events_table_${YEAR}.txt html/combine_plots/syst_shape_plot/
        else
          python plotSyst.py ${BOSON} ${CHANNEL} ${YEAR} ${FLAG}
        fi
      done
      echo ""
    done
  done
done
