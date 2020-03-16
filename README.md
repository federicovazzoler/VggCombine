# VggCombine
Combine scripts for the Vgg analysis

To set up the package (before cloning this repo!):

export SCRAM_ARCH=slc7_amd64_gcc700

cmsrel CMSSW_10_2_13

cd CMSSW_10_2_13/src

cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit

git fetch origin

git checkout v8.0.2

cd $CMSSW_BASE/src

bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-https.sh)

scramv1 b clean; scramv1 b

git clone git@github.com:federicovazzoler/VggCombine.git

link your html directory
