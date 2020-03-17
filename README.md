# VggCombine
Combine scripts for the Vgg analysis

Please refer to this tutorial: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HCombExercise

To set up the package (before cloning this repo!):

`cmsrel CMSSW_10_2_13`

`cd CMSSW_10_2_13/src`

`cmsenv`

`git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit`

`cd HiggsAnalysis/CombinedLimit`

`git fetch origin`

`git checkout v8.0.2`

`cd $CMSSW_BASE/src`

`bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-https.sh)`

`scramv1 b clean; scramv1 b`

`git clone git@github.com:federicovazzoler/VggCombine.git`

link your html directory

create all the needed datacards
