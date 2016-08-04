#!/usr/bin/env python

# DV_analysisScriptsRun2
import BasicConfig
import RunConfig
import MaterialVolume

import sys

# import ROOT and AtlasStyle
try:
    import ROOT
    import AtlasStyle
except ImportError:
    # on my laptop
    sys.path.append('/usr/local/root/latest/lib')
    sys.path.append(workdir + 'Macro/')
    import ROOT
    import AtlasStyle

def OpenTFile(filepath):
    tfile = ROOT.TFile(filepath, 'open')
    if tfile.IsOpen():
        print(filepath + ' is opened successfully!')
    else:
        print(filepath + ' failed to be opened!')
        sys.exit()
    return tfile

if __name__ == "__main__":
    # Configure ROOT as Atlas Style
    AtlasStyle.SetAtlasStyle()

    #
    filename_DVMultiTrkBkg = 'all.root' if RunConfig.year == 2015 else 'all_2016.root'

    # Material Volume
    if RunConfig.doMaterialVolume:
        matVol = MaterialVolume.MaterialVolume()
        if RunConfig.doCalcMV:
            matVol.calculateMaterialVolume()
        if RunConfig.doShowMR:
            canvas = ROOT.TCanvas("c", "c", 1000, 600)
            matVol.showMaterialRegions(canvas)
        if RunConfig.doEstiHI:
            tf = OpenTFile(BasicConfig.workdir + filename_DVMultiTrkBkg)
            matVol.estimateHadronicInteractions(tf)

