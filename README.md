# VggCombine
Combine scripts for the Vgg analysis

Please refer to this tutorial: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HCombExercise

and to this presentation: https://indico.cern.ch/event/747340/contributions/3198653/attachments/1744339/2823486/HComb-Tutorial-FitDiagnostics.pdf

New combine version available (01-04-2020): https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/releases/tag/v8.1.0

If you have already installed combine v8.0.2 simply update to v8.1.0:

`cd HiggsAnalysis/CombinedLimit`

`git fetch origin`

`git checkout v8.1.0`

`scramv1 b clean; scramv1 b`

To set up the package (before cloning this repo!):

`export SCRAM_ARCH=slc7_amd64_gcc700`

`cmsrel CMSSW_10_2_13`

`cd CMSSW_10_2_13/src`

`cmsenv`

`git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit`

`cd HiggsAnalysis/CombinedLimit`

`git fetch origin`

`git checkout v8.1.0`

`cd $CMSSW_BASE/src`

`bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-https.sh)`

`scramv1 b clean; scramv1 b`

`git clone git@github.com:federicovazzoler/VggCombine.git`

link your html directory

create all the needed datacards
