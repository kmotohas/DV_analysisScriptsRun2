
#from ROOT import TFile
from ROOT import TTree
from ROOT import TH1F

from ROOT import TCanvas
from ROOT import kGray
from ROOT import kPink

#from ROOT import gPad

import AtlasStyle

import BasicConfig
import utils

from datetime import date


if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()

    directory = '/Volumes/HDPX-UTA/data/mc15_13TeV/'
    systTree = [
        #utils.open_tfile(BasicConfig.rootcoredir + 'systTree_302137.root'),
        #utils.open_tfile(directory + 'systTree_group.phys-susy.402715.PythiaRhad_AUET2BCTEQ6L1_gen_gluino_p1_1200_qq_100_1ns.recon.ESD.e4732_s2821_s2183_r6869.trkvrt.v1_EXT0.root'),
        utils.open_tfile(directory + 'systTree_mc15_13TeV.402074.PythiaRhad_AUET2BCTEQ6L1_gen_gluino_p1_1200_qq_100_1ns.recon.DAOD_RPVLL.e4620_s2770_s2183_r8788.root'),
        #utils.open_tfile(BasicConfig.rootcoredir + 'systTree_307732.root')
        utils.open_tfile(directory + 'DVPlusMETSys/systTree_mc15_13TeV.402074.PythiaRhad_AUET2BCTEQ6L1_gen_gluino_p1_1200_qq_100_1ns.merge.DAOD_SUSY15.e4620_s2770_s2183_r8788_p2877.root')
        ]
    nominal = [TTree(), TTree()]
    hist = [TH1F(), TH1F()]
    #legend1 = 'run302137 (group-susy)'
    #legend1 = 'mc15a from ESD (g1200 chi100 1ns)'
    legend1 = 'r8788 mc15c from HITS (g1200 chi100 1ns)'
    #legend2 = 'run307732 (central)'
    legend2 = 'p2877 mc15c from HITS (g1200 chi100 1ns)'

    systTree[0].GetObject('Nominal', nominal[0])
    systTree[1].GetObject('Nominal', nominal[1])

    #utils.compare_two_ntuples(nominal[0], nominal[1], 'DV_chisqPerDOF', 100, 0, 5,
    #                          'DV_chisqPerDOF < 5 && DV_passFidCuts && DV_passMatVeto', legend1, legend2)
    utils.compare_two_ntuples(nominal[0], nominal[1], 'MET', 400, 0, 2000, '', legend1, legend2)
    utils.compare_two_ntuples(nominal[0], nominal[1], 'MET_TST', 20, 0, 100, '', legend1, legend2)
    #utils.compare_two_ntuples(nominal[0], nominal[1], 'Jets_nocalib_pT', 100, 0, 500, '', legend1, legend2)
    #utils.compare_two_ntuples(nominal[0], nominal[1], 'DV_m', 100, 0, 20,
    #                          'DV_m < 20 && DV_passFidCuts && DV_passMatVeto', legend1, legend2)
    #utils.compare_two_ntuples(nominal[0], nominal[1], 'sqrt(DV_x*DV_x+DV_y*DV_y)', 300, 0, 300,
    #                          'DV_passFidCuts', legend1, legend2, 'DV_r')

    #c = TCanvas('c', 'c', 900, 800)
    #c.SetLogy(0)  # False
    #c.SetLogz(1)  # True
    #nominal[1].Draw("DV_chisqPerDOF:sqrt(DV_x*DV_x+DV_y*DV_y)",
    #                "DV_chisqPerDOF < 5 && DV_passFidCuts && DV_passMatVeto", "colz")
    #utils.save_as(c, BasicConfig.plotdir + 'validation/' + str(date.today()) + '/DV_chisq_vs_r_' + legend1)
    #nominal[0].Draw("DV_y:DV_x>>h_xy0(600,-300,300,600,-300,300)", "DV_passFidCuts", "colz")
    #utils.save_as(c, BasicConfig.plotdir + 'validation/' + str(date.today()) + '/DV_xy_' + legend1)
    #nominal[1].Draw("DV_y:DV_x>>h_xy1(600,-300,300,600,-300,300)", "DV_passFidCuts", "colz")
    #utils.save_as(c, BasicConfig.plotdir + 'validation/' + str(date.today()) + '/DV_xy_' + legend2)
