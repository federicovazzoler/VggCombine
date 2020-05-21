# VggCombine
Combine scripts for the Vgg analysis

### Content

1. [INFO](#1-INFO)
1. [How to install](#2-How-to-install)
1. [How to run](#3-How-to-run)
1. [Advanced use](#4-Advanced-use)

### 1. INFO

Please refer to this tutorial: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HCombExercise

and to this presentation: https://indico.cern.ch/event/747340/contributions/3198653/attachments/1744339/2823486/HComb-Tutorial-FitDiagnostics.pdf

New combine version available (01-04-2020): https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/releases/tag/v8.1.0

### 2. How to install

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

### 3. How to run

To run the tool:

(use the correct folder for the theo uncertainties and eventually modify the path in run_them_all.sh)

`cmsenv`

`./run_them_all [plot version]`

### 4. Advanced use

#### Checks on Fit Diagnostic

Some useful checks to be done on Fit Diagnostic results can be found here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks

##### When a nuisance is costrained by the fit

If one of the nuisances (X) is quite heavily constrained or has a post-fit uncertainty >1 you should try to scan this nuisance parameter using:

`combine -M MultiDimFit workspace.root --algo grid -P X --points 1000 --setParameterRanges X=-3,3`

To see if there are double minima in the scan open the root file and launch:

`limit->Draw("deltaNLL:X")`

##### Diagnose fit procedure with toys

Diagnose the fitting procedure in toy experiments following: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#toy-by-toy-diagnostics
