#!/usr/bin/env python

import BasicConfig
#BasicConfig = BasicConfig.BasicConfig()
from datetime import date

#try:
import ROOT
import AtlasStyle
#except ImportError:
#    # on my laptop
#
#    sys.path.append('/usr/local/root/latest/lib')
#    sys.path.append(BasicConfig.workdir + 'Macro/')
#    import ROOT
#    import AtlasStyle

class MaterialVolume:
    def __init__(self):
        self.module_name = 'MV'
        self.tf = ROOT.TFile(BasicConfig.rootcoredir
                             + "DVAnalyses/data/materialMap3D_Run2_v2.1.1.root", "open")
        self.matMap = ROOT.TH3D()
        self.tf.GetObject("map", self.matMap)
        self.nr = self.matMap.GetNbinsX()
        self.np = self.matMap.GetNbinsY()
        self.nz = self.matMap.GetNbinsZ()
        self.min_r = self.matMap.GetXaxis().GetBinLowEdge(1)
        self.min_p = self.matMap.GetYaxis().GetBinLowEdge(1)
        self.min_z = self.matMap.GetZaxis().GetBinLowEdge(1)
        self.max_r = self.matMap.GetXaxis().GetBinLowEdge(self.nr+1)
        self.max_p = self.matMap.GetYaxis().GetBinLowEdge(self.np+1)
        self.max_z = self.matMap.GetZaxis().GetBinLowEdge(self.nz+1)
        self.dr = float(self.max_r - self.min_r) / self.nr
        self.dp = float(self.max_p - self.min_p) / self.np
        self.dz = float(self.max_z - self.min_z) / self.nz
        self.region_list = [22., 25., 29., 38., 46.,
                            73., 84., 111., 120., 145.,
                            180., 300.]

    def passMaterialVeto(self, r, phi, z):
        if self.matMap.GetBinContent(self.matMap.FindBin(r, phi, z)) == 0:
            return True
        else:
            return False

    def getRegion(self, r, nonMaterial):
        if   r < self.region_list[0]:
            return 0
        elif r < self.region_list[1]:
            return 1
        elif r < self.region_list[2]:
            return 2
        elif r < self.region_list[3]:
            return 3
        elif r < self.region_list[4]:
            return 4
        elif r < self.region_list[5]:
            return 5
        elif r < self.region_list[6]:
            return 6
        elif r < self.region_list[7]:
            return 7
        elif r < self.region_list[8]:
            return 8
        elif r < self.region_list[9]:
            return 9
        elif r < self.region_list[10]:
            return 10
        elif r < self.region_list[11]:
            return 11
        else:
            return -1

    def dV(self, r, dr, dphi, dz):
        # triangle approximation
        inner = 0.5 * (r-dr) * ((r-dr) * dphi) * dz
        outer = 0.5 * r * (r * dphi) * dz
        return outer - inner
        #return dr * (r * dphi) * dz

    def printProgress(self, materialVolume, nonMaterialVolume):
        print("MaterialVolume: {}".format(materialVolume))
        print("nonMaterialVolume: {}".format(nonMaterialVolume))
        print("sum: {}".format(nonMaterialVolume + materialVolume))
        print("material ratio: {}".format(materialVolume/(nonMaterialVolume+materialVolume)*100.))

    def calculateMaterialVolume(self):
        print '*** start MaterialVolume.calculateMaterialVolume'
        materialVolume = 0.
        nonMaterialVolume = 0.
        for ir in range(1, self.nr+1):
            r = self.min_r + self.dr * ir
            if not (ir % 10):
                print(ir, self.nr)
                self.printProgress(materialVolume,nonMaterialVolume)
            for ip in range(1, self.np+1):
                phi = self.min_p + self.dp * ip
                for iz in range(1, self.nz+1):
                    z = self.min_z + self.dz * iz
                    if self.passMaterialVeto(r, phi, z):
                        nonMaterialVolume += self.dV(r, self.dr, self.dp, self.dz)
                    else:
                        materialVolume += self.dV(r, self.dr, self.dp, self.dz)
        fullVolume = ROOT.TMath.Pi() * 300 * 300 * 600
        self.printProgress(materialVolume,nonMaterialVolume)

    def showMaterialRegions(self, canvas):
        print '*** start MaterialVolume.showMaterialRegions'
        canvas.cd()
        matRegion = ROOT.TH2F("matRegion", ";Z [mm];R [mm]",
                         self.nz, -300, 300, self.nr, 0, 300)
        gStyle.SetPalette(42)
        matRegion.SetContour(12)
        for ir in range(1,self.nr+1):
            r = (self.matMap.GetXaxis().GetBinLowEdge(ir)
                 + self.matMap.GetXaxis().GetBinLowEdge(ir+1)) / 2.
            for iz in range(1,self.nz+1):
                z = (self.matMap.GetZaxis().GetBinLowEdge(iz)
                     + self.matMap.GetZaxis().GetBinLowEdge(iz+1)) / 2.
                nonMaterial = self.passMaterialVeto(r, 0, z)
                rIndex = self.getRegion(r, nonMaterial)
                matRegion.Fill(z, r, rIndex)
        matRegion.SetMinimum(-0.5)
        matRegion.SetMaximum(11.5)
        matRegion.Draw("colz")
        canvas.SaveAs(BasicConfig.plotdir + self.module_name
                      + "_materialRegion_{}.png".format(date.today()))
        canvas.SaveAs(BasicConfig.plotdir + self.module_name
                      + "_materialRegion_{}.pdf".format(date.today()))

    def estimateHadronicInteractions(self, tfile, ntrk=3):
        """
        obsolete
        """
        print '*** start MaterialVolume.estimateHadronicInteractions'
        densityAir = 1.3e-3 # [g/cm3]
        densitySilicon = 2.3
        matVolRatio = 0.42
        massDists = []
        vetoedRegions = [1, 3, 5, 7, 9]
        nonVetoedRegions = [0, 2, 4, 6, 8, 10, 11]
        if not isinstance(ntrk, int):
            ntrk = int(ntrk)
        nVetoedVertices = 0
        nNonVetoedVertices = 0
        prefix = "BkgEst_data_{}Trk_Region".format(ntrk)
        suffix = "_DVMultiTrkBkg"
        for ii in range(len(vetoedRegions)+len(nonVetoedRegions)):
            massDists.append(ROOT.TH1F())
            tfile.GetObject(prefix+str(ii)+suffix, massDists[ii])
            if ii in vetoedRegions:
                nVetoedVertices += massDists[ii].GetEntries()
            else:
                nNonVetoedVertices += massDists[ii].GetEntries()
        print("Number of Vertices in vetoed regions: {}".format(nVetoedVertices))
        est = nVetoedVertices * (densityAir / densitySilicon) * (1 - matVolRatio)
        print("Estimated nHadInt in non-vetoed regions: {}".format(est))
        print("Number of Vertices in non-vetoed regions: {}".format(nNonVetoedVertices))
        print("Ratio: {}".format(est/nNonVetoedVertices))

if __name__ == "__main__":
    matVol = MaterialVolume()
    # config
    #doCalcMV = False
    doCalcMV = True
    doShowMR = False
    doEstiHI = False
    year = 2016
    #
    if doCalcMV:
        matVol.calculateMaterialVolume()
    if doShowMR:
        AtlasStyle.SetAtlasStyle()
        canvas = ROOT.TCanvas("c", "c", 1000, 600)
        matVol.showMaterialRegions(canvas)
    if doEstiHI:
        filename = 'all.root' if year == 2015 else 'all_2016.root'
        tf = ROOT.TFile(BasicConfig.workdir + filename, "open")
        if not tf.IsOpen():
            import sys
            print(BasicConfig.workdir + filename + ' failed to be opened!')
            sys.exit()
        matVol.estimateHadronicInteractions(tf)
